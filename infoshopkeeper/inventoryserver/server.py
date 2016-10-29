#!/usr/bin/python
# coding: UTF-8
import cherrypy
import os
import sys
import re
import string
import uuid
import logging
import logging.handlers

from mx.DateTime import now

from Cheetah.Template import Template
from simplejson import JSONEncoder

import turbojson
import json

import isbnlib

from MySQLdb import escape_string

import os.path
current_dir = os.path.dirname(os.path.abspath(__file__))

from sqlobject.sqlbuilder import *
from sqlobject.dberrors import DuplicateEntryError

#Class that manages dictionary of menu items.
#Format for adding a menu:
#   {'1': [('menu display title', 'menu action', [ 'submenu of same triplet format' ]), ]}
#The dictionary is so that different webapps can add menus in any and it's not dependent on
#load order of apps. No way yet to cause two webapps to both add to same menu
class MenuData:
    menuData={}
   
    @classmethod
    def getMenuData(cls):
        return [MenuData.menuData[key] for key in sorted(MenuData.menuData.keys())] 
    
    @classmethod
    def setMenuData(cls, dictionaryOfMenuLists):
        MenuData.menuData.update(dictionaryOfMenuLists)
     


from tools import db
from tools import inventory

from objects.author import Author
from objects.book import Book
from objects.category import Category
from objects.kind import Kind
from objects.location import Location
from objects.notes import Notes
from objects.special_order import SpecialOrder
from objects.title import Title
from objects.title_special_order import TitleSpecialOrder
from objects.transaction import Transaction

from IndexTemplate import IndexTemplate
from SearchTemplate import SearchTemplate
from BookEditTemplate import BookEditTemplate
from TitleEditTemplate import TitleEditTemplate
from TitleListTemplate import TitleListTemplate
from AuthorEditTemplate import AuthorEditTemplate
from CategoryEditTemplate import CategoryEditTemplate
from ChooseItemForISBNTemplate import ChooseItemForISBNTemplate
from ChooseItemTemplate import ChooseItemTemplate
from KindEditTemplate import KindEditTemplate
from KindListTemplate import KindListTemplate
from LocationEditTemplate import LocationEditTemplate
from LocationListTemplate import LocationListTemplate
from NotesTemplate import NotesTemplate
from ReportListTemplate import ReportListTemplate
from ReportTemplate import ReportTemplate
from TransactionsTemplate import TransactionsTemplate
from CartTemplate import CartTemplate
from CartTemplate2 import CartTemplate2
from CheckoutTemplate import CheckoutTemplate
from StaffingCalendarTemplate import StaffingCalendarTemplate
from AddToInventoryTemplate import AddToInventoryTemplate
from SpecialOrderEditTemplate import SpecialOrderEditTemplate
from SpecialOrderItemEditTemplate import SpecialOrderItemEditTemplate
from SpecialOrderListTemplate import SpecialOrderListTemplate
from SelectSpecialOrderTemplate import SelectSpecialOrderTemplate

from config.config import configuration

from printing import barcode_monkeypatch
from printing import barcodeLabel
from printing import specialOrderLabel

#decorator function to return json
turbojson.jsonify._instance=turbojson.jsonify.GenericJSON(ensure_ascii=False)
def jsonify_tool_callback(*args, **kwargs):
    #print>>sys.stderr, "in jsonify"
    cherrypy.response.headers['Content-type'] = 'application/json; charset=utf-8'
    body=turbojson.jsonify.encode(cherrypy.response.body).encode('utf-8')
    #print>>sys.stderr, "body changed ", body
    cherrypy.response.headers['Content-length']=len(body)
    cherrypy.response.body=body
cherrypy.tools.jsonify = cherrypy.Tool('before_finalize', jsonify_tool_callback, priority=30)

#flag for when admin and special_orders load.
#use it to turn on & off printing and special order checking
#depending on whether we are local or not. I hate this. Better way?
admin_loaded = False
special_order_loaded=False

#Noteboard app
class Noteboard:
    def __init__(self):
        self._notestemplate = NotesTemplate()
        self.menudata=MenuData
        MenuData.setMenuData({'6':('Notes', '/notes/noteboard', [])}) 
   
    #handler for noteboard template call   
    @cherrypy.expose
    def noteboard(self):
        return self._notestemplate.respond()
    
    #get all notes in Notes and format as list of uls
    @cherrypy.expose
    @cherrypy.tools.jsonify()
    def get_notes(self, **kwargs):
        notes=[['<ul><li>%s</li><li>%s</li><li>%s</li></ul>' % (n.author, n.whenEntered, n.message)] for n in Notes.select().orderBy('-id')]
        return notes
        
    #post note to database
    @cherrypy.expose
    def post_note(self, author='', message='', **kwargs):
        if kwargs:
            #print "kwargs are ", kwargs
            pass
        if author:
            if message:
                #print "author & message are ", author, " ", message
                Notes(author=author,  message=message)
                return self._notestemplate.respond()
        if kwargs['author']:
            if kwargs['message']:
                #print "using kwargs to add note"
                Notes(author=kwargs['author'], message=kwargs['message'])

#Class for register   
class Register:
    def __init__(self):
        self._carttemplate = CartTemplate2()
        self._chooseitemtemplate = ChooseItemTemplate()
        self.menudata=MenuData
        MenuData.setMenuData( {'1': ('Remove Items from Inventory', '/register/build_cart', []) })

    #return cart template    
    @cherrypy.expose
    def build_cart(self, **args):
        self._carttemplate.session_data=cherrypy.session.get('cart')
        return self._carttemplate.respond()
    
    #actually add items to cart
    @cherrypy.expose
    def add_item_to_cart(self, **args):
        print>>sys.stderr, "IN add_item_to_cart     ARGS ARE"
        print>>sys.stderr, 'cart ', args, repr(args)
        cart={}
        print>>sys.stderr, "CART SESSION IS: ", cherrypy.session.id
        
        #check to see if there's a cart & get it
        if cherrypy.session.has_key('cart'):
            print>>sys.stderr, "CART EXISTS"         
            cart = cherrypy.session.pop('cart')
            if 'uuid' not in cart:
                cart['uuid']= cart['uuid']=uuid.uuid1().hex
        #or make a cart. id is hes uuid
        else:
            print>>sys.stderr, "MAKE CART" 
            cart['uuid']=uuid.uuid1().hex
        print>>sys.stderr, "CART IS ", cart
        #if there's no list of items start one
        if not cart.has_key('items'):
            print>>sys.stderr, "MAKE CART ITEM ARRAY"
            cart['items']=[]
        
        #add item to item key list
        if args.has_key('item'):
            print>>sys.stderr, "add_item_to_cart: in item block", json.loads(args['item'])
            cart['items'].append(json.loads(args['item']))
            cherrypy.session['cart']=cart
            print>>sys.stderr, cart
        elif args.has_key('titleid'):
            print>>sys.stderr, "add_item_to_cart: in titleid block", args['titleid']
            prev_same_title=[]
            for previous_item in cart['items']:
                if str(previous_item['titleID'])==args['titleid']:
                    prev_same_title.append(previous_item['bookID'])
            b=Book.select(Book.q.titleID==args['titleid'] ).filter(Book.q.status=='STOCK')
            if args.has_key('ourprice'):
                print>>sys.stderr, "filtering by price"
                b=b.filter(Book.q.ourprice==float(args['ourprice']))
            if prev_same_title:
                print>>sys.stderr, "filtering by not same copy"
                b=b.filter(NOT(IN(Book.q.id, prev_same_title)))
            if b.count()>0:
                b=b[0]       
                print>>sys.stderr, 'add_item_to_cart: book is', b
                item={'bookID':b.id, 'titleID':b.titleID, 'booktitle':b.title.booktitle, 'isbn':b.title.isbn, 'ourprice':b.ourprice, 'department':b.title.kind.kindName.capitalize(), 'isInventoried':True, 'isTaxable':True}
                cart['items'].append(item)
        print>>sys.stderr, "CART IS NOW ", cart
        cherrypy.session['cart']=cart
        #have to save or it all gets forgot
        print>>sys.stderr, cart, cherrypy.session['cart']
        cherrypy.session.save()
        hooks = cherrypy.serving.request.hooks['before_finalize']
        forbidden = cherrypy.lib.sessions.save
        hooks[:] = [h for h in hooks if h.callback is not forbidden]
        print>>sys.stderr, "CART NOW IS: ", cherrypy.session['cart']
        print>>sys.stderr, "CART SESSION NOW IS: ", cherrypy.session.id
        return None
            
    @cherrypy.expose
    def remove_item_from_cart(self, **args):
        #print>>sys.stderr, "args are ", args
        #print>>sys.stderr, type(int(args['index']))
        #print>>sys.stderr, int(args['index'])        
        
        #arg should be index number of item we want to ditch
        item_index=int(args['index'])
        cart={}
        #is there a cart?
        if cherrypy.session.has_key('cart'):
            cart=cherrypy.session['cart']
            #print>>sys.stderr, cart, cart['items'], cart['items'][item_index]
        #if so, are there items in it?
        if cart.has_key('items'):
            print>>sys.stderr, "has items"
            #pop item number n
            cart['items'].pop(item_index)
            print>>sys.stderr, cart
        cherrypy.session['cart']=cart
        cherrypy.session.save()
        hooks = cherrypy.serving.request.hooks['before_finalize']
        forbidden = cherrypy.lib.sessions.save
        hooks[:] = [h for h in hooks if h.callback is not forbidden]
            
    #ditch the whole cart
    @cherrypy.expose
    def void_cart(self):
        if cherrypy.session.has_key('cart'):
            cherrypy.session['cart']={}
        cherrypy.session.save()        
        hooks = cherrypy.serving.request.hooks['before_finalize']
        forbidden = cherrypy.lib.sessions.save
        hooks[:] = [h for h in hooks if h.callback is not forbidden]
    
    #check out cart
    @cherrypy.expose
    def check_out(self, **args):
        cart={}
        #is there a cart?
        if cherrypy.session.has_key('cart'):
            cart=cherrypy.session['cart']
            #does it have items?
            if cart.has_key('items'):
                shouldRaiseException=False

                #make a shallow copy of cart to iterate on
                #for is a generator, so it gets confused
                #if you iterate on a list you're removing items from.
                cart_items_copy = cart['items'][:]
                for item in cart_items_copy:
                    #if it is an inventoried item
                    #mark item sold, record transaction
                    #and remove from cart
                    print>>sys.stderr, "checkout: item is ", item
                    if item.get('bookID'):
                        try:
                            print>>sys.stderr, "preparing to sell book"
                            print>>sys.stderr, "bookID is", item.get('bookID')
                            b=Book.selectBy(id=item['bookID'])[0]
                            b.set(status='SOLD', sold_when=now().strftime("%Y-%m-%d"))
                            if item.get('special_order_selected'):
                                tso=TitleSpecialOrder.get(item['special_order_selected']) 
                                tso.orderStatus='SOLD'
                                print>>sys.stderr, tso
                                print>>sys.stderr, 'special order marked sold'
                           
                            print>>sys.stderr, "book is ", b
                            infostring = "'[] " + item['department']
                            if item.has_key('booktitle'):
                                infostring=infostring + ": " +item['booktitle']
                            print>>sys.stderr, 'About to do transaction'
                            Transaction(action='SALE', info=infostring, owner=None, cashier=None, schedule=None, amount=item['ourprice'], cartID=cart.get('uuid', ''))
                            cart['items'].remove(item)
                            print>>sys.stderr, "Item removed from cart"
                        except Exception as err:
                            print>>sys.stderr, "error in selling book", err
                            # problemItems.append(item)
                            shouldRaiseException=True
                    #if it's a noninventoried item just 
                    #record transaction and remove from cart
                    else:
                        try:
                            infostring = "'[] " + item['department']
                            if item.has_key('booktitle'):
                                infostring=infostring + ": " +item['booktitle']
                            Transaction(action='SALE', date=now(), info=infostring, owner=None, cashier=None, schedule=None, amount=float(item['ourprice']), cartID=cart.get('uuid', ''))
                            cart['items'].remove(item)
                        except Exception as err:
                            print>>sys.stderr, "error in selling book", err
                            # problemItems.append(item)
                            shouldRaiseException=True
            #it should be zero but just in case
            #there was an error, items with error are still kept
            try:
                print>>sys.stderr, 'cart length is now ', len(cart['items'])
            except KeyError:
                print>>sys.stderr, 'cart is now', cart
            if cart['items'].__len__()==0:
                cherrypy.session['cart']={}
            else:
                cherrypy.session['cart']=cart
            #save cart 
            cherrypy.session.save()
            hooks = cherrypy.serving.request.hooks['before_finalize']
            forbidden = cherrypy.lib.sessions.save
            hooks[:] = [h for h in hooks if h.callback is not forbidden]
            #raise the delayed exception
            if shouldRaiseException:
                raise sqlobject.SQLObjectNotFound
                                    
    @cherrypy.expose
    @cherrypy.tools.jsonify()
    def get_cart(self):
        return [cherrypy.session.get('cart')]
    
    #search for in stock items by attribute
    @cherrypy.expose
    def select_item_search(self, title="",sortby="booktitle",isbn="",distributor="",owner="",publisher="",author="",category="", tag="",kind="",location="", authorOrTitle=""):
        self._chooseitemtemplate.should_show_images = configuration.get('should_show_images')
        self._chooseitemtemplate.empty=True
        self._chooseitemtemplate.title=title
        self._chooseitemtemplate.isbn=isbn
        self._chooseitemtemplate.author=author
        self._chooseitemtemplate.category=category
        self._chooseitemtemplate.distributor=distributor
        self._chooseitemtemplate.owner=owner
        self._chooseitemtemplate.publisher=publisher 
        self._chooseitemtemplate.tag=tag
        self._chooseitemtemplate.locations=list(Location.select(orderBy="location_name"))
        self._chooseitemtemplate.location=location
        the_location=location
        if type(the_location)==type([]):
            the_location=the_location[0]
        self._chooseitemtemplate.authorOrTitle=authorOrTitle
        self._chooseitemtemplate.kinds=list(Kind.select())
        self._chooseitemtemplate.kind=kind
        the_kind=kind
        if type(the_kind) == type([]):
            the_kind=the_kind[0]
        self._chooseitemtemplate.table_is_form=True
        
        titles=[]
        
        #used to check that any filtering is done
        fields=[title,author,category,distributor,owner,isbn,publisher,tag,kind,authorOrTitle]
        fields_used = [f for f in fields if f != ""]
        
        #start out with the join clauses in the where clause list
        where_clause_list = []
        #only search for in stock books
        where_clause_list.append("book.status='STOCK'")
        clause_tables=['book', 'author', 'author_title', 'category', 'location']
        join_list=[LEFTJOINOn('title', 'book', 'book.title_id=title.id'), LEFTJOINOn(None, 'author_title', 'title.id=author_title.title_id'), LEFTJOINOn(None, 'author', 'author.id=author_title.author_id'), LEFTJOINOn(None, Category, Category.q.titleID==Title.q.id), LEFTJOINOn(None, Location, Location.q.id==Book.q.locationID)]

        #add filter clauses if they are called for
        if the_kind:
            where_clause_list .append("title.kind_id = '%s'" % escape_string(the_kind))
        if the_location and len(the_location)>1:
            where_clause_list .append("book.location_id = '%s'" % escape_string(the_location))
        if title:
            where_clause_list.append("title.booktitle RLIKE '%s'" % escape_string(title.strip()))
        if publisher:
            where_clause_list.append("title.publisher RLIKE '%s'" % escape_string(publisher.strip()))
        if tag:
            where_clause_list.append("title.tag RLIKE '%s'" % escape_string(tag.strip()))
        if isbn:
            where_clause_list.append("title.isbn RLIKE '%s'" % escape_string(isbn))
        if owner:
            where_clause_list.append("book.owner RLIKE '%s'" % escape_string(owner.strip()))
        if distributor:
            where_clause_list.append("book.distributor RLIKE '%s'" % escape_string(distributor.strip()))
        if author:
            where_clause_list.append("author.author_name RLIKE '%s'" % escape_string(author.strip()))
        if category:
            where_clause_list.append("category.category_name RLIKE '%s'" % escape_string(category.strip()))
        if authorOrTitle:
            print>>sys.stderr, "in authorOrTitle ", authorOrTitle
            where_clause_list.append("(author.author_name RLIKE '%s' OR title.booktitle RLIKE '%s')" % (escape_string(authorOrTitle.strip()), escape_string(authorOrTitle.strip())))

        #AND all where clauses together
        where_clause=' AND '.join(where_clause_list)
        print>>sys.stderr, 'where clause ', where_clause
        titles=[]

        #do search. 
        if len(fields_used)>0:
            titles=Title.select( where_clause,join=join_list,clauseTables=clause_tables,orderBy=sortby,distinct=True)
            print>>sys.stderr, titles.queryForSelect()
        print>>sys.stderr, "titles ", list(titles)
        self._chooseitemtemplate.titles=titles
        return self._chooseitemtemplate.respond()

    #search by isbn to find item
    @cherrypy.expose
    @cherrypy.tools.jsonify()
    def get_item_by_isbn(self,   **kwargs):
        print>>sys.stderr, 'kwargs are', kwargs
        isbn=kwargs.get('isbn', '')
        print>>sys.stderr, isbn
        #strip spaces and quotes from isbn string
        isbn=isbn.replace('\"', '')
        price=0
        if len(isbn) in (15,17,18) and isbn[-5] == '5':
            price = float(isbn[-4:])/100
            isbn=isbn[:-5]
        if len(isbn) in (15,17,18) and isbn[-5] != '5':
                    isbn=isbn[:-5]
        if ( len(isbn)==10 and isbnlib.is_isbn10(isbn)):
            isbn=isbnlib.to_isbn13(isbn)
        #search for isbn
        titlelist = Title.selectBy(isbn=isbn)
        
        #if we find it search for associated books in stock
        if titlelist.count():
            booklist = titlelist.throughTo.books.filter(Book.q.status=='STOCK').orderBy([-Book.q.ourprice, Book.q.inventoried_when])

            #search for book that has the proper price if price is given.
            #otherwise, fall back to just returning the oldest book.
            if price:
                booklist = booklist.filter(Book.q.ourprice==price)

            if booklist.count():
         
                so=[[tso.id, tso.specialOrder.customerName] for tso in booklist.throughTo.title.throughTo.specialorder_pivots.filter(TitleSpecialOrder.q.orderStatus=='ON HOLD SHELF')]

                result_dict = {}
                for b in booklist:
                        if result_dict.has_key(b.ourprice):
                            if result_dict[b.ourprice]['inventoried_when'] > b.inventoried_when:
                                result_dict[b.ourprice] = {'titleID':b.title.id, 'booktitle':b.title.booktitle, 'isbn':b.title.isbn, 'bookID':b.id, 'ourprice':b.ourprice, 'inventoried_when':b.inventoried_when, 'special_orders':so}
                        else:
                            result_dict[b.ourprice] = {'titleID':b.title.id, 'booktitle':b.title.booktitle, 'isbn':b.title.isbn, 'bookID':b.id, 'ourprice':b.ourprice, 'inventoried_when':b.inventoried_when, 'special_orders':so}
           
                        print>>sys.stderr, booklist, result_dict, so
                #oldest_b = min(result_dict.itervalues(), key=lambda x: x["inventoried_when"])
                #return [oldest_b]
                print>>sys.stderr, result_dict
                return [result_dict]
            #if there's no in stock books 
            else:
                return []
        #if we don't have title
        else:
            return []
 
#Use Google staffing calendar to fill schedule 
class Staffing:
    def __init__(self):
        self._staffingcalendartemplate = StaffingCalendarTemplate()
        self.menudata = MenuData

    #hook for staffing calendar template
    @cherrypy.expose
    def calendar(self, **args):
        print>>sys.stderr, "in calendar ", self._staffingcalendartemplate.respond() 
        return self._staffingcalendartemplate.respond()


#Administrative tasks
class Admin:
    def __init__(self):
        self._kindedittemplate = KindEditTemplate()
        self._kindlisttemplate = KindListTemplate()
        self._locationedittemplate = LocationEditTemplate()
        self._locationlisttemplate = LocationListTemplate()
        self._add_to_inventory_template=AddToInventoryTemplate()
        self._chooseitemforisbntemplate=ChooseItemForISBNTemplate()
             
        #set flag to true. 
        #currently, we use this to enable printing.
        admin_loaded = True
         
        MenuData.setMenuData({'3': ('Add to Inventory', '/admin/add_to_inventory', [])})
        #notice trac is on here but it's run out of its own wsgi script
        MenuData.setMenuData({'7':('Admin', '', [  ('Edit Item Kinds', '/admin/kindlist', []),
                                                   ('Edit Item Locations', '/admin/locationlist', []),
                                                   ('Bug Reports/Issues', 'javascript:document.location=&#39http://&#39+document.location.hostname+&#39:8030&#39+&#39/trac/newticket&#39;', []),
                                                 ])})
     
    #hook for kind edit template
    @cherrypy.expose
    def kindedit(self,**args):
        #print args
        if ('kindName' in args.keys()):
            self._kindedittemplate.kind=Kind.form_to_object(Kind,args)
            return self.kindlist()
        else:
            self._kindedittemplate.kind=Kind.form_to_object(Kind,args)
            return self._kindedittemplate.respond()
     
    #hook for kind list template
    @cherrypy.expose    
    def kindlist(self,**args):
        self._kindlisttemplate.kinds=list(Kind.select())
        return self._kindlisttemplate.respond()
     
    #hook for location edit template
    @cherrypy.expose
    def locationedit(self,**args):
        if ('locationName' in args.keys()):
            self._locationedittemplate.location=Location.form_to_object(Location,args)
            return self.locationlist()
        else:
            self._locationedittemplate.location=Location.form_to_object(Location,args)
            return self._locationedittemplate.respond()
     
    #hook for location list template
    @cherrypy.expose
    def locationlist(self,**args):
        self._locationlisttemplate.locations=list(Location.select(orderBy="location_name"))
        return self._locationlisttemplate.respond()
     
    #hook for add to inventory template
    @cherrypy.expose
    def add_to_inventory(self, isbn="", orig_isbn='', large_url='', med_url='', small_url='', quantity=1, title="", listprice='0.00', ourprice='0.00', authors="", publisher="", categories="", distributor="", location="", owner=configuration.get('default_owner'), status="STOCK", tag="", kind=configuration.get('default_kind'), type='', known_title=False, printlabel=False, num_copies=1):
        self._add_to_inventory_template.isbn=isbn
        self._add_to_inventory_template.orig_isbn=orig_isbn
        self._add_to_inventory_template.large_url=large_url
        self._add_to_inventory_template.med_url=med_url
        self._add_to_inventory_template.small_url=small_url
        self._add_to_inventory_template.quantity=quantity
        self._add_to_inventory_template.title=title
        self._add_to_inventory_template.authors=authors
        self._add_to_inventory_template.listprice=listprice
        self._add_to_inventory_template.ourprice=ourprice
        self._add_to_inventory_template.publisher=publisher
        self._add_to_inventory_template.categories=categories

        conn=Book._connection
        query=Select( Book.q.distributor, groupBy=Book.q.distributor)
        results=conn.queryAll( conn.sqlrepr(query))
        distributorlist=[t[0] for t in results] 
        self._add_to_inventory_template.distributors=distributorlist
        self._add_to_inventory_template.distributor=distributor 
        self._add_to_inventory_template.locations=list(Location.select(orderBy="location_name"))
        self._add_to_inventory_template.location=location
        self._add_to_inventory_template.owner=owner
        self._add_to_inventory_template.status=status
        self._add_to_inventory_template.tag=tag
        self._add_to_inventory_template.kinds=list(Kind.select())
        self._add_to_inventory_template.kind=kind
        self._add_to_inventory_template.printlabel=printlabel

        conn=Title._connection
        query=Select( Title.q.type, groupBy=Title.q.type)
        results=conn.queryAll( conn.sqlrepr(query))
        typelist=[t[0] for t in results] 
        self._add_to_inventory_template.formats=typelist
        self._add_to_inventory_template.format=type
        self._add_to_inventory_template.known_title=known_title
        return self._add_to_inventory_template.respond()
         
    #prints label for item. needs printer info to be set up in etc.
    @cherrypy.expose
    def print_label(self, isbn='', booktitle='', authorstring='',ourprice='0.00', listprice='0.00', num_copies=1):
        barcodeLabel.print_barcode_label(isbn=isbn, booktitle=booktitle, ourprice=ourprice, listprice=listprice, num_copies=num_copies)
        #%pipe%'lpr -P $printer -# $num_copies -o media=Custom.175x120'
        #find out where gs lives on this system; chop off /n
        #p = subprocess.Popen(["which", "gs"], stdout=subprocess.PIPE)
        #out, err = p.communicate()
        #gs_location=out.strip()
        #print_command_string = string.Template(u"export TMPDIR=$tmpdir; $gs_location -q -dSAFER -dNOPAUSE -sDEVICE=pdfwrite -sprice='$ourprice' -sisbnstring='$isbn' -sbooktitle='$booktitle' -sauthorstring='$authorstring' -sOutputFile=%pipe%'lpr -P $printer -# $num_copies -o media=Custom.175x120' barcode_label.ps 1>&2")
        #if isbn and booktitle and ourprice:
            #print>>sys.stderr, authorstring
            #print>>sys.stderr,  print_command_string.substitute(
            #    {'gs_location':gs_location, 'booktitle': booktitle.replace("'", " ").encode('utf8', 'backslashreplace'), 'authorstring': authorstring.replace("'", " ").encode('utf8', 'backslashreplace'), 'isbn':isbn, 'ourprice':ourprice, 
           #         'num_copies':num_copies, 'printer':etc.label_printer_name, 'tmpdir':tempfile.gettempdir()})
            #pcs_sub=print_command_string.substitute(
            #    {'gs_location':gs_location, 'booktitle': booktitle.replace("'", " "), 'authorstring': authorstring.replace("'", " "), 'isbn':isbn, 'ourprice':ourprice, 
             #       'num_copies':num_copies, 'printer':etc.label_printer_name, 'tmpdir':tempfile.gettempdir()})
            #subprocess.call( pcs_sub.encode('utf8'), shell=True, cwd=os.path.dirname(os.path.abspath(__file__)))


    #get next isbn in series that we are using for in-house labels`
    #I've gone through great lengths to make sure there's no collision, but there's still a
    #bit of a fiat clause to the EAN organization.
    @cherrypy.expose
    def get_next_unused_local_isbn(self):
        try:
            result = Title.select("title.isbn RLIKE \'^199[0-9]{10}$'").max(Title.q.isbn)
        except:
            result= '199' + '0'*10
        result= unicode(int(result[:-1])+1) + isbnlib._core._check_digit13(unicode(int(result[:-1])+1))
        return result

    #wrapper to inventory.addToInventory to be added
    #after a few minor manipulations. Ditches dollar sign, makes 
    #prices floats and turns categories & authors into lists
    @cherrypy.expose
    def add_item_to_inventory(self, **kwargs):
        print>>sys.stderr, "in add_item_to_inventory"
        print>>sys.stderr, "kwargs are:"
        print>>sys.stderr, kwargs
        kwargs['listprice']=float(kwargs['listprice'].replace('$', ''))
        kwargs['ourprice']=float(kwargs['ourprice'].replace('$', ''))
        kwargs['authors']=kwargs['authors'].split(',')
        kwargs['categories'] = kwargs['categories'].split(',')
        if (kwargs['known_title'] == 'False' or kwargs['known_title'] == 'false'):
            kwargs['known_title']=False
        else:
            try:
                kwargs['known_title'] = list(Title.selectBy(isbn=kwargs['isbn']).orderBy("id").limit(1))[0]
            except:
                kwargs['known_title']=False
        print "kwargs are now", kwargs
        kwargs['kind_name']=kwargs['kind']
        print kwargs
        try:
            inventory.addToInventory(**kwargs)
        except Exception as e:
            print>>sys.stderr, e
                 
    #wrapper to inventory.search_inventory
    #looks for an item in database, if we don't have it, 
    #looks in amazon
    @cherrypy.expose
    @cherrypy.tools.jsonify()
    def search_isbn(self, **args):
        print>>sys.stderr, 'search_isbn args ', args
        data=inventory.lookup_by_isbn(args['isbn'])
        print>>sys.stderr, 'data', data

        most_freq_location=''
        if (data and data['known_title']):
            most_freq_location = data['known_title']._connection.queryAll(
            '''SELECT book.location_id FROM title JOIN book ON book.title_id=title.id WHERE title.isbn='%s' AND book.location_id !=1 GROUP BY title.isbn, book.location_id ORDER BY count(book.location_id) DESC LIMIT 1''' % data['known_title'].isbn
            )
            if most_freq_location:            
                data['most_freq_location'] = most_freq_location[0][0]
            max_price=list(data['known_title']._connection.queryAll(
            '''SELECT MAX(book.listprice) FROM title JOIN book ON book.title_id=title.id WHERE title.isbn='%s' GROUP BY title.isbn''' % data['known_title'].isbn
            ))
            if max_price:
                max_price='{0:.2f}'.format(max_price[0][0])
            else:
                max_price='0.00'
            data['listprice'] = data['ourprice'] = max_price
            print>>sys.stderr, 'data modified. new data are ', data
        return [data]
    add_to_inventory.search_isbn=search_isbn

    @cherrypy.expose
    @cherrypy.tools.jsonify()
    def search_id(self, titleid):
        print>>sys.stderr
        title=Title.get(titleid)
        if title:
            #queryAll returns lists of lists for results
            most_freq_location=title._connection.queryAll(
            '''SELECT book.location_id FROM book WHERE book.title_id=%s AND book.location_id !=1 GROUP BY book.title_id, book.location_id ORDER BY count(book.location_id) DESC LIMIT 1''' % title.id
            )
            if most_freq_location:
                most_freq_location=most_freq_location[0][0]
            else:
                most_freq_location=''
            max_price=list(title._connection.queryAll(
            '''SELECT MAX(book.listprice) FROM book WHERE book.title_id=%s GROUP BY book.title_id''' % title.id
            ))
            if max_price:
                max_price='{0:.2f}'.format(max_price[0][0])
            else:
                max_price='0.00'
        print>>sys.stderr,  most_freq_location, max_price, title
        #return [{'isbn':title.isbn, 'title': title.booktitle, 'location':most_freq_location,'listprice':max_price, 'ourprice':max_price, 'known_title':True}]
        return [{'isbn':title.isbn, 'orig_isbn':title.origIsbn, 'title':title.booktitle, 'listprice':max_price, 'ourprice':max_price, 'authors':title.authors_as_string(), 'publisher':title.publisher, 'categories':title.categories_as_string(), 'location':most_freq_location, 'kind':title.kindID, 'type':title.type, 'known_title':True}]

    #search for in stock items by attribute
    @cherrypy.expose
    def select_item_for_isbn_search(self, title="",sortby="booktitle",isbn="",distributor="",owner="",publisher="",author="",category="", tag="",kind="",location=""):
        self._chooseitemforisbntemplate.empty=True
        self._chooseitemforisbntemplate.title=title
        self._chooseitemforisbntemplate.should_show_images = configuration.get('should_show_images')
        self._chooseitemforisbntemplate.isbn=isbn
        self._chooseitemforisbntemplate.author=author
        self._chooseitemforisbntemplate.category=category
        self._chooseitemforisbntemplate.distributor=distributor
        self._chooseitemforisbntemplate.owner=owner
        self._chooseitemforisbntemplate.publisher=publisher 
        self._chooseitemforisbntemplate.tag=tag
        self._chooseitemforisbntemplate.locations=list(Location.select(orderBy="location_name"))
        self._chooseitemforisbntemplate.location=location
        the_location=location
        if type(the_location)==type([]):
            the_location=the_location[0]
        self._chooseitemforisbntemplate.kinds=list(Kind.select())
        self._chooseitemforisbntemplate.kind=kind
        the_kind=kind
        if type(the_kind) == type([]):
            the_kind=the_kind[0]
        self._chooseitemforisbntemplate.table_is_form=True
         
        titles=[]
         
        #used to check that any filtering is done
        fields=[title,author,category,distributor,owner,isbn,publisher,tag,kind]
        fields_used = [f for f in fields if f != ""]
         
        #start out with the join clauses in the where clause list
        where_clause_list = ["book.title_id=title.id", "author_title.title_id=title.id", "author_title.author_id=author.id", "category.title_id=title.id"]
         
        #add filter clauses if they are called for
        if the_kind:
            where_clause_list .append("title.kind_id = '%s'" % escape_string(the_kind))
        if the_location and len(the_location)>1:
            where_clause_list .append("book.location_id = '%s'" % escape_string(the_location))
        if title:
            where_clause_list.append("title.booktitle RLIKE '%s'" % escape_string(title.strip()))
        if publisher:
            where_clause_list.append("title.publisher RLIKE '%s'" % escape_string(publisher.strip()))
        if tag:
            where_clause_list.append("title.tag RLIKE '%s'" % escape_string(tag.strip()))
        if isbn:
            where_clause_list.append("title.isbn RLIKE '%s'" % escape_string(isbn))
        if owner:
            where_clause_list.append("book.owner RLIKE '%s'" % escape_string(owner.strip()))
        if distributor:
            where_clause_list.append("book.distributor RLIKE '%s'" % escape_string(distributor.strip()))
        if author:
            where_clause_list.append("author.author_name RLIKE '%s'" % escape_string(author.strip()))
        if category:
            where_clause_list.append("category.category_name RLIKE '%s'" % escape_string(category.strip()))
         
        #AND all where clauses together
        where_clause=' AND '.join(where_clause_list)
        titles=[]
         
        #do search. 
        if len(fields_used)>0:
            titles=Title.select( where_clause,orderBy=sortby,clauseTables=['book','author','author_title', 'category'],distinct=True)
                 
        self._chooseitemforisbntemplate.titles=titles
        return self._chooseitemforisbntemplate.respond()
        
class SpecialOrders:
    
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self._special_order_edit_template = SpecialOrderEditTemplate()
        self._special_order_list_template = SpecialOrderListTemplate()
        self._special_order_item_edit_template =  SpecialOrderItemEditTemplate()
        self._select_special_order_template = SelectSpecialOrderTemplate()
        self.conn=db.connect()
        
        #let package know special order is loaded
        special_order_loaded=True

        MenuData.setMenuData({'4': ('Special Order', '/specialorder/special_order_list', [])})

    #special order list template
    @cherrypy.expose
    def special_order_list(self, customer_name="", customer_phone_number='', customer_email='', title="",sortby="customer_name",isbn="",author="", kind=""):
        self._special_order_list_template.empty=True
        self._special_order_list_template.customer_name=customer_name
        self._special_order_list_template.customer_phone_number=customer_phone_number
        self._special_order_list_template.customer_email=customer_email
        self._special_order_list_template.title=title
        self._special_order_list_template.isbn=isbn
        self._special_order_list_template.author=author
        self._special_order_list_template.kinds=list(Kind.select())
        self._special_order_list_template.kind=kind
        the_kind=kind
        if type(the_kind) == type([]):
            the_kind=the_kind[0]
        self._special_order_list_template.table_is_form=True
        
        titles=[]
        
        #used to check that any filtering is done
        fields=[customer_name, customer_phone_number, customer_email,title,author,isbn,kind]
        fields_used = [f for f in fields if f != ""]
        
        #start out with the join clauses in the where clause list
        where_clause_list = []
        clause_tables=['title_special_order', 'title', 'author', 'author_title', ]
        join_list=[LEFTJOINOn('special_order', 'title_special_order', 'title_special_order.special_order_id=special_order.id'), LEFTJOINOn(None, 'title', 'title.id=title_special_order.title_id'), LEFTJOINOn(None, 'author_title', 'title.id=author_title.title_id'), LEFTJOINOn(None, 'author', 'author_title.author_id=author.id')]
        
        #add filter clauses if they are called for
        if customer_name:
            where_clause_list.append("special_order.customer_name RLIKE '%s'" % escape_string(customer_name.strip()))
        if customer_phone_number:
            where_clause_list.append("special_order.customer_phone_number RLIKE '%s'" % escape_string(customer_phone_number.strip()))
        if customer_email:
            where_clause_list.append("special_order.customer_email RLIKE '%s'" % escape_string(customer_email.strip()))
        if the_kind:
            where_clause_list .append("(title.kind_id = '%s' OR title.kind_id IS NULL)" % escape_string(the_kind))
        if title:
            where_clause_list.append("title.booktitle RLIKE '%s'" % escape_string(title.strip()))
        if isbn:
            where_clause_list.append("title.isbn RLIKE '%s'" % escape_string(isbn))
        if author:
            where_clause_list.append("author.author_name RLIKE '%s'" % escape_string(author.strip()))
        where_clause=None
        if len(where_clause_list) > 0:
            #AND all where clauses together
            where_clause=' AND '.join(where_clause_list)
        orders=[]
        #do search.
        orders=SpecialOrder.select( where_clause,join=join_list,clauseTables=clause_tables,orderBy=sortby,distinct=True)
        self._special_order_list_template.orders=orders
        return self._special_order_list_template.respond()

    def common(self):
        for x in [getattr(self,x) for x in dir(self) if 'template' in x]:
            x.lastsearch=cherrypy.session.get('lastsearch',False)

    #hook to special order edit template
    @cherrypy.expose
    def special_order_edit(self,**args):
        self.common()
        self._special_order_edit_template.specialorder=SpecialOrder.form_to_object(SpecialOrder,args)
        return self._special_order_edit_template.respond()
    
    #hook to special order item edit template
    @cherrypy.expose
    def special_order_item_edit(self, **args):
        self._special_order_item_edit_template.special_order_item=TitleSpecialOrder.form_to_object(TitleSpecialOrder, args)
        return self._special_order_item_edit_template.respond()
    
    #hook to select_specialorder template
    #simple table of results for authorOrTitle search
    #from database and amazon. Uses inventory.search_by_keyword
    #which returns an itereator. Only does the first 100 for now.
    #Hope to figure out how to do a paged ajax call.
    @cherrypy.expose
    def select_special_order_search(self, authorOrTitle='', special_order='', **args):
        self.common()
        self._select_special_order_template.authorOrTitle = authorOrTitle
        self._select_special_order_template.specialOrderID = special_order
        resultset = self._select_special_order_template.resultset = {}
        keyword_search_iter = inventory.search_by_keyword(authorOrTitle=authorOrTitle)
        while len(resultset) <20:
            try:
                search_result = keyword_search_iter.next()
                if not resultset.has_key( search_result['isbn'] ):
                    resultset[search_result['isbn']] = search_result
            except StopIteration:
                break
        return self._select_special_order_template.respond()
    
    
    #add special order.
    #First we check to see if we know the book
    #and add it to inventory if we don't;
    #then we add the book to the special order
    @cherrypy.expose
    def add_to_special_order(self, **args):
        print>>sys.stderr, "in add to spec order", args
        if args.get('item'):
            print>>sys.stderr,  args.get('item')
            item=json.loads(args.get('item'))
            print>>sys.stderr,  "known_title is", item.get('known_title', '')
            if item.get('known_title'):
                print>>sys.stderr, 'know_titles id key is', item.get('known_title')['id']
            print>>sys.stderr, 'known_title_id is', item.get('known_title_id', '')
            known_title=''
            if item.get('known_title_id'):
                known_title= Title.get( int(item.get('known_title_id')))
            elif item.get('known_title'):
                known_title=Title.get(int(item.get('known_title')['id']))
            else:
                inventory.addToInventory(title=item['booktitle'], authors=item['authors'], isbn=item['isbn'], categories=item['categories'], quantity=0, known_title=known_title, kind_name='kind', types=item['types'])
                known_title=Title.selectBy(isbn=item['isbn'])
            TitleSpecialOrder(titleID=known_title.id, specialOrderID=args.get('specialOrderID'))
        return

    #change status of special order items
    @cherrypy.expose
    def set_special_order_item_status(self, **args):
        print>>sys.stderr, "set_spec_order_args", args
        if (args.get('special_orders') and args.get('status')):
            special_orders=json.loads(args.get('special_orders'))
            print>>sys.stderr, special_orders
            if type(special_orders) == type(u''):
                special_orders=[special_orders]
            for so in special_orders:
                TitleSpecialOrder.get(int(so)).orderStatus=args['status']

class CSLogging:
    def __init__(self):
        self.client_side_logger = logging.getLogger('ClientSideLogger')
        self.client_side_logger.setLevel(logging.DEBUG)
        handler = logging.handlers.RotatingFileHandler("/var/log/infoshopkeeper/ClientSideError.log", maxBytes=100000, backupCount=5)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.client_side_logger.addHandler(handler)

    @cherrypy.expose
    def logger(self, url='', message='', linenumber=0, browser='', counter=0, level='', sid=''):
        log_command=self.client_side_logger.error
        if level=="Error":
            log_command=self.client_side_logger.error
        elif level=='Warn':
            log_command=self.client_side_logger.warning
        elif level=='info':
            log_command=self.client_side_logger.info
        elif level=='debug':
            log_command=self.client_side_logger.debug
        log_command('{url}\t{line}{message} {browser}'.
              format(**{'url':url, 'line':(
                       'line {linenumber}\t'.format(linenumber=linenumber) if linenumber else ''), 'message':message, 'browser':browser}))

  
class InventoryServer:
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
  
        self.reportlist=[getattr(__import__('reports.'+x,globals(),{},[1]),x) for x in configuration.get("reports")]
 
         
        self._indextemplate = IndexTemplate()
        self._carttemplate = CartTemplate()
        self._checkouttemplate = CheckoutTemplate()
        self._searchtemplate = SearchTemplate()
        self._bookedittemplate = BookEditTemplate()
        self._authoredittemplate = AuthorEditTemplate()
        self._categoryedittemplate = CategoryEditTemplate()
        self._titleedittemplate = TitleEditTemplate()
        self._titlelisttemplate = TitleListTemplate()
        self._reportlisttemplate = ReportListTemplate()
        self._reporttemplate = ReportTemplate()
        self._transactionstemplate = TransactionsTemplate()
        self._special_order_edit_template = SpecialOrderEditTemplate()
        self._special_order_list_template = SpecialOrderListTemplate()
        self._special_order_item_edit_template =  SpecialOrderItemEditTemplate()  
        self._select_special_order_template = SelectSpecialOrderTemplate()
        self.conn=db.connect()
         
        MenuData.setMenuData({'2': ('Search the Inventory', '/search', [])})
        MenuData.setMenuData({'5': ('Reports', '/reports',
                                        [(i.metadata['name'], '/report?reportname=' + i.metadata['action'], []) for i in self.reportlist])})
     
    def loadUserByUsername(self, login):
        ulist=[("woodenshoebooks","woodenshoe"), ]
        for u,p in ulist:
            if u==login:
                return (u,p)
            else:
                pass
 
    def checkLoginAndPassword(self, login, password):
        user = self.loadUserByUsername(login)
        if user==None:
            return u'Wrong login/password'
        elif user[0] == login:
            if user[1] != password:
                return u'Wrong login/password'
            else:
                cherrypy.request.login = cherrypy.session.get("sessid", login)
 
                 
    def common(self):
        for x in [getattr(self,x) for x in dir(self) if 'template' in x]:
            x.lastsearch=cherrypy.session.get('lastsearch',False)
     
    #hook to index template
    @cherrypy.expose
    def index(self,**args):
        self.common()
        return self._indextemplate.respond()
     
    #hook to book edit template
    @cherrypy.expose
    def bookedit(self,**args):
        self.common()
        self._bookedittemplate.book=Book.form_to_object(Book,args)
        return self._bookedittemplate.respond()
    
    #data source for jquery autocomplete widget for author field
    @cherrypy.expose
    @cherrypy.tools.jsonify()
    def author_autocomplete(self, **args):
        term=args.get('term')
        print>>sys.stderr, "term is", term
        if term:
            results=[ results.authorName for results in Author.select("author.author_name RLIKE '%s' LIMIT 20" % term)]
            print>>sys.stderr, results
            return results

    #data source for jquery autocomplete widget for title field
    @cherrypy.expose
    @cherrypy.tools.jsonify()
    def title_autocomplete(self, **args):
        term=args.get('term')
        print>>sys.stderr, "term is", term
        if term:
            results=[ results.booktitle for results in Title.select("title.booktitle RLIKE '%s' LIMIT 20" % term)]
            print>>sys.stderr, results
            return results
     
    #hook to author edit template
    @cherrypy.expose
    def authoredit(self,**args):
        print>>sys.stderr, "in  authoredit", args, args.get('id'), args.get('title_id')
        self.common()
        self._authoredittemplate.author=None
        self._authoredittemplate.new_author=False
        self._authoredittemplate.title_id=args.get('title_id')
        print>>sys.stderr, self._authoredittemplate.title_id
        if args.has_key('id'):
            self._authoredittemplate.new_author=False
            if not args.get('delete'):
                print>>sys.stderr, "in edit author", self._authoredittemplate.author
                try:
                    self._authoredittemplate.author=Author.form_to_object(Author,args)
                #                 self._authoredittemplate.author.addTitle(Title.get(args['title_id']))
                except DuplicateEntryError as e:
                    a=Author.selectBy(authorName=args['authorName'])[0]
                    try:
                        a.addTitle(Title.get(args['title_id']))
                    except DuplicateEntryError as e:
                        pass
                    self._authoredittemplate.author=a
                return self._authoredittemplate.respond()       
            else:
                Author.delete(args.get('id'))
                return self._indextemplate.respond()
        elif args.get('new_author'):
            self._authoredittemplate.new_author=True
            self._authoredittemplate.title_id=args.get('title_id')
            return self._authoredittemplate.respond()
     
    #hook to category edit template
    @cherrypy.expose
    def categoryedit(self,**args):
        self.common()
        self._categoryedittemplate.category=Category.form_to_object(Category,args)
        return self._categoryedittemplate.respond()
     
    #hook to title edit template
    @cherrypy.expose
    def titleedit(self,**args):
        self.common()
        self._titleedittemplate.should_show_images = configuration.get('should_show_images')
        
        print>>sys.stderr, args
        title=Title.get(args.get('id')) 
        if args.get('remove_author'):
            title.removeAuthor(args.get('author_id'))
        self._titleedittemplate.title=Title.form_to_object(Title,args)
        return self._titleedittemplate.respond()
        
    #hook to title list template
    @cherrypy.expose
    def titlelist(self,**args):
        self.common()
        self._titlelisttemplate.titles=[]
        try:
            if (type(args['titles']) is types.UnicodeType) or (type(args['titles']) is types.StringType):
                #print int(args['titles'])
                self._titlelisttemplate.titles.append(Title.get(int(args['titles'])))
                #print self._titlelisttemplate.titles
            else:
                for id in args['titles']:
                    self._titlelisttemplate.titles.append(Title.get(int(id)))
                #print self._titlelisttemplate.titles
        except KeyError:
            pass
 
        try: 
            if (args['delete']):
            #delete the titles
                for title in self._titlelisttemplate.titles:
                    for author in title.authors:
                        Author.delete(author.id)
                    for book in title.books:
                        Book.delete(book.id)
                    for category in title.categorys:
                        Category.delete(category.id)
                     
                    Title.delete(title.id)
 
            #and back to the search
                from cherrypy.lib import httptools
                httptools.redirect(cherrypy.session['lastsearch'])  
        except:
            return self._titlelisttemplate.respond()
    #search for in stock items by attribute
    #wrapper to inventory.search_inventory
    #looks for an item in database, if we don't have it, 
    #looks in amazon
    @cherrypy.expose
    @cherrypy.tools.jsonify()
    def search_isbn(self, **args):
        data=inventory.lookup_by_isbn(args['isbn'])
        
        copies_in_stock = 0
        if data:
            d = data.get('known_title')
            if d:
                copies_in_stock=d.copies_in_status('STOCK')
        data['copies_in_stock'] = copies_in_stock
        return [data]            
     
    #old checkout template
    @cherrypy.expose
    def checkout(self,**args):
        self.common()
        self._checkouttemplate.status_from=args.get("status_from","STOCK")
        self._checkouttemplate.status_to=args.get("status_to","RETURNED")
        self._checkouttemplate.schedules = [("list price",1)]+configuration.get("multiple_prices")
 
         
        if "change" in args:
            return self.addtocart(**args)
        if "finalize" in args:
            schedule_name=args["schedule"]
            #print configuration
            #print configuration.get("multiple_prices")
            schedule=[x for x in configuration.get("multiple_prices")+[("list price",1)] if x[0]==schedule_name] 
            schedule_price=schedule[0][1]
            receipt=""
            for q in cherrypy.session.get('quantities',[]):
 
                original=q[0]
                howmany=q[1]
                 
                for copy in list(Book.select(AND(Book.q.titleID==original.titleID,Book.q.status=="STOCK",Book.q.listprice==original.listprice)))[0:howmany]:
                    cursor=self.conn.cursor()
                    cursor.execute("""
                        INSERT INTO transactionLog SET
                        action = "SALE",
                        amount = %s,
                        cashier = %s,
                        date = NOW(),
                        info = %s,
                        schedule = %s,
                        owner = %s
                        """,(copy.listprice * schedule_price,args["cashier"],"[%s] %s" % (copy.distributor,copy.title.booktitle),schedule_name,copy.owner))
                    copy.sellme()
                    cursor.close()
                line_pt_1 =  "%s  X  %s  @ $%.2f * %i%%" % (original.title.booktitle[:25],howmany,original.listprice,schedule_price * 100)
                receipt=receipt+string.ljust(line_pt_1,50)+string.rjust("$%.2f" % (howmany*schedule_price*original.listprice),10)
            return receipt
         
        if "restatus" in args and "status_to" in args and "status_from" in args:
            for q in cherrypy.session.get('quantities',[]):
                original=q[0]
                howmany=q[1]
                for copy in list(Book.select(AND(Book.q.titleID==original.titleID,Book.q.status==args["status_from"],Book.q.listprice==original.listprice)))[0:howmany]:
                     
                    copy.status=args["status_to"]
                     
            cherrypy.session['quantities']=[]
 
        if "delete" in args:
            for q in cherrypy.session.get('quantities',[]):
                original=q[0]
                original_price=original.listprice
                original_status=original.status
                original_title_id=original.titleID
                howmany=q[1]
                for copy in list(Book.select(AND(Book.q.titleID==original_title_id,Book.q.status==original_status,Book.q.listprice==original_price)))[0:howmany]:
                    Book.delete(copy.id)
            cherrypy.session['quantities']=[]
 
             
         
        self._checkouttemplate.quantities=cherrypy.session.get('quantities',[])
        return self._checkouttemplate.respond()
     
    #old add to cart function
    @cherrypy.expose
    def addtocart(self,**args):
        self.common() 
         
        if args.get('reset_quantities')=="true":
            cherrypy.session['quantities']=[]
 
        #these are multiple copies of the same book
        for a in args.keys():
            match=re.compile("^select_x_like_(\d+)").match(a)
            if match:
                try:
                    number_of_copies_to_sell=int(args[a])
                    id=match.group(1)
                    original=Book.get(id)
                    try:
                        quantities=cherrypy.session.get('quantities',[])
                        quantities.append((original,number_of_copies_to_sell))
                        cherrypy.session['quantities']=quantities
                    except:
                        pass
 
                except Exception,e:
                    #print str(e)
                    pass
 
        #these are checked individual copies
        copy_ids=[]
        try:
            if type(args['copy_id'])==type([0,1]):
                for copy_id in args['copy_id']:
                    copy_ids.append(copy_id)
            else:
                copy_ids.append(args['copy_id'])
        except:
            pass
 
        for copy_id in copy_ids:
            quantities=cherrypy.session.get('quantities',[])
            quantities.append((Book.get(copy_id),1))
            cherrypy.session['quantities']=quantities
 
        if "checkout" in args:
            return self.checkout(**args)
        else:
            self._carttemplate.quantities=cherrypy.session.get('quantities',[])
            return self._carttemplate.respond()    
     
    #search by attribute
    @cherrypy.expose
    def search(self,id='', title="",sortby="booktitle",isbn="",distributor="",owner="",publisher="",author="",category="",out_of_stock='no',stock_less_than="",stock_more_than="",sold_more_than="", sold_begin_date="",sold_end_date="",inv_begin_date='',inv_end_date='', tag="",kind="",location="", formatType=""):
        cherrypy.session['lastsearch']=False
        self.common()
        cherrypy.session['lastsearch']=cherrypy.url()
        
        self._searchtemplate.empty=True
        self._searchtemplate.title=title
        self._searchtemplate.should_show_images = configuration.get('should_show_images')
        self._searchtemplate.isbn=isbn
        self._searchtemplate.author=author
        self._searchtemplate.category=category
        self._searchtemplate.distributor=distributor
        self._searchtemplate.owner=owner
        self._searchtemplate.publisher=publisher
        self._searchtemplate.out_of_stock=out_of_stock
        self._searchtemplate.stock_less_than=stock_less_than
        self._searchtemplate.stock_more_than=stock_more_than
        self._searchtemplate.sold_more_than=sold_more_than
        self._searchtemplate.inv_begin_date=inv_begin_date
        self._searchtemplate.inv_end_date=inv_end_date
        self._searchtemplate.sold_begin_date=sold_begin_date
        self._searchtemplate.sold_end_date=sold_end_date
        self._searchtemplate.tag=tag
        #find locations for dropdown
        self._searchtemplate.locations=list(Location.select(orderBy="location_name"))
        self._searchtemplate.location=location
        the_location=location
        if type(the_location)==type([]):
            the_location=the_location[0]
 
        #find formats of items for dropdown
        #it's more complicated because we only want the type field
        conn=Title._connection
        query=Select( Title.q.type, groupBy=Title.q.type)
        results=conn.queryAll( conn.sqlrepr(query))
        formatTypelist=[t[0] for t in results]
        self._searchtemplate.formats=formatTypelist
        self._searchtemplate.formatType=formatType
         
        #get list of kinds for dropdown
        self._searchtemplate.kinds=list(Kind.select())
        self._searchtemplate.kind=kind
        the_kind=kind
        if type(the_kind) == type([]):
            the_kind=the_kind[0]
         
        #find out if fields are used or if we are filtering on
        #in stock
        titles=[]
        fields=[id,title,author,category,distributor,owner,isbn,publisher,stock_less_than,stock_more_than,sold_more_than,inv_begin_date,inv_end_date,sold_begin_date,sold_end_date,tag,kind]
        fields_used = [f for f in fields if f != ""]
         
        #start building the filter list
        where_clause_list = []
        clause_tables=['book', 'author', 'author_title', 'category', 'location']
        join_list=[LEFTJOINOn('title', 'book', 'book.title_id=title.id'), LEFTJOINOn(None, 'author_title', 'title.id=author_title.title_id'), LEFTJOINOn(None, 'author', 'author.id=author_title.author_id'), LEFTJOINOn(None, Category, Category.q.titleID==Title.q.id), LEFTJOINOn(None, Location, Location.q.id==Book.q.locationID)]
        if the_kind:
            where_clause_list .append("title.kind_id = '%s'" % escape_string(the_kind))
        if the_location and len(the_location)>1:
            where_clause_list .append("book.location_id = '%s'" % escape_string(the_location))
        if title:
            where_clause_list.append("title.booktitle RLIKE '%s'" % escape_string(title.strip()))
        if publisher:
            where_clause_list.append("title.publisher RLIKE '%s'" % escape_string(publisher.strip()))
        if tag:
            where_clause_list.append("title.tag RLIKE '%s'" % escape_string(tag.strip()))
        if isbn:
            isbn, price=inventory.process_isbn(isbn)
            where_clause_list.append("title.isbn RLIKE '%s'" % escape_string(isbn))
        if formatType:
            where_clause_list.append("title.type RLIKE '%s'" % escape_string(formatType.strip()))
        if owner:
            where_clause_list.append("book.owner RLIKE '%s'" % escape_string(owner.strip()))
        if distributor:
            where_clause_list.append("book.distributor RLIKE '%s'" % escape_string(distributor.strip()))
        if inv_begin_date:
            where_clause_list.append("book.inventoried_when >= '%s'" % escape_string(inv_begin_date))
        if inv_end_date:
            where_clause_list.append("book.inventoried_when < '%s'" % escape_string(inv_end_date))
        if sold_begin_date:
            where_clause_list.append("book.sold_when >= '%s'" % escape_string(sold_begin_date))
        if sold_end_date:
            where_clause_list.append("book.sold_when < '%s'" % escape_string(sold_end_date))
        if author:
            where_clause_list.append("author.author_name RLIKE '%s'" % escape_string(author.strip()))
        if category:
            where_clause_list.append("category.category_name RLIKE '%s'" % escape_string(category.strip()))
        if id:
            where_clause_list.append("title.id=%s" % escape_string(id))
        where_clause=' AND '.join(where_clause_list)
         
        #do search first. Note it currently doesnt let you search for every book in database, unless you use some sort of
        #trick like '1=1' for the where clause string, as the where clause string may not be blank
        titles=[]
        if len(fields_used)>0 or out_of_stock=="yes":
            titles=Title.select( where_clause,join=join_list, orderBy=sortby,clauseTables=clause_tables,distinct=True)
        #filter for stock status
        if out_of_stock == 'yes':
                    titles = [t for t in titles if t.copies_in_status("STOCK") == 0]
        #filter on specific numbers in stock
        if stock_less_than != "":
            titles = [t for t in titles if t.copies_in_status("STOCK") <= int(stock_less_than)]
        if stock_more_than != "":
            titles = [t for t in titles if t.copies_in_status("STOCK") >= int(stock_more_than)]
        #filter by items sold
        if sold_more_than != "":
            titles = [t for t in titles if t.copies_in_status("SOLD") >= int(sold_more_than)]
        self._searchtemplate.titles=titles
        return  self._searchtemplate.respond()            

    #old transactions template
    @cherrypy.expose    
    def transactions(self,**args):
        self.common()
        begin_date=args.get('begin_date','')
        end_date=args.get('end_date','')
        what=args.get('what','')
        action=args.get('action','SALE')
        deleteid=args.get('deleteid','0')
        if int(deleteid) >0:
            Transaction.delete(deleteid)
        
        
        self._transactionstemplate.begin_date=begin_date
        self._transactionstemplate.end_date=end_date
        self._transactionstemplate.what=what
        self._transactionstemplate.action=action
 
        self._transactionstemplate.transactions=[]
        if begin_date and end_date:
            self._transactionstemplate.transactions=list(Transaction.select("""
        transactionLog.date >= '%s' AND
        transactionLog.date <= ADDDATE('%s',INTERVAL 1 DAY) AND
        transactionLog.info LIKE '%%%s%%' AND
        transactionLog.action LIKE '%%%s%%'
                """ % (escape_string(begin_date),escape_string(end_date),escape_string(what),escape_string(action))))
     
        return  self._transactionstemplate.respond()
 
         
    #hook to list of reports
    @cherrypy.expose
    def reports(self,**args):
        self.common()
        self._reportlisttemplate.reports=[r.metadata for r in self.reportlist]
        return  self._reportlisttemplate.respond()
     
    #hook to the specific report template
    @cherrypy.expose
    def report(self,**args):
        self.common()
        #get report data by name
        the_report=[r for r in self.reportlist if r.metadata['action']==args['reportname']][0](args)
        #set report template to correct template
        self._reporttemplate.report=the_report
         
        #get results if query done
        if args.get('query_made','no')=='yes':
            self._reporttemplate.do_query=True
            results=the_report.query(args)
            if the_report.show_header:
                self._reporttemplate.header=the_report.format_header()
            self._reporttemplate.results=the_report.format_results(results)
            if the_report.do_total:
                self._reporttemplate.total=the_report.get_total(results)
            else:
                self._reporttemplate.total=0
        #or naked template otherwise
        else:
            self._reporttemplate.do_query=False
             
        return  self._reporttemplate.respond()
        
    @cherrypy.expose
    def test(self):
        return '''
                <link type="text/css" href="/javascript/css/smoothness/jquery-ui-1.8.13.custom.css" rel="Stylesheet" />	
                <script type='text/javascript' src='/javascript/jquery-1.12.3.min.js'></script>
                <script type='text/javascript' src='/javascript/jquery.dataTables.js'></script>
                <script type='text/javascript' src='/javascript/FixedHeader.js'></script>
                <script type='text/javascript' src='/javascript/jquery-ui-1.9.1.custom/js/jquery-ui-1.9.1.custom.js'></script>

                <body><table class="sortable dataTable" id="message_table" aria-describedby="message_table_info"><thead><tr role="row"><th class="sorting" role="columnheader" tabindex="0" aria-controls="message_table" rowspan="1" colspan="1" style="width: 1004px; " aria-label="Notes&amp;nbsp;&amp;nbsp;&amp;nbsp;: activate to sort column ascending"><a href="#" class="sortheader" onclick="ts_resortTable(this);return false;">Notes<span class="sortarrow">&nbsp;&nbsp;&nbsp;</span></a></th></tr></thead><tbody role="alert" aria-live="polite" aria-relevant="all"><tr class="odd"><td class=""><ul><li>Lou</li><li>2012-10-03 12:14:56</li><li>Start at 5469</li></ul></td></tr><tr class="even"><td class=""><ul><li>Lou</li><li>2012-08-12 18:23:29</li><li>Start at 5468</li></ul></td></tr><tr class="odd"><td class=""><ul><li>Zen</li><li>2012-08-07 16:59:43</li><li>Fugazi - Repeater was purchased, marked "REG 5456" on sleeve, in inventory marked "REG 4472"</li></ul></td></tr><tr class="even"><td class=""><ul><li>Zen</li><li>2012-08-05 18:31:55</li><li>Sold a copy of "Soccer vs. the State," which is not listed in ISK --Zen, 8/5/12</li></ul></td></tr><tr class="odd"><td class=""><ul><li>Lou</li><li>2012-07-28 17:09:25</li><li>Start at 5461</li></ul></td></tr><tr class="even"><td class=""><ul><li>test</li><li>2012-07-20 13:57:18</li><li>test</li></ul></td></tr><tr class="odd"><td class=""><ul><li>test</li><li>2012-07-20 13:06:53</li><li>test</li></ul></td></tr><tr class="even"><td class=""><ul><li>Lou</li><li>2012-06-13 17:56:27</li><li>Start at 5360</li></ul></td></tr><tr class="odd"><td class=""><ul><li>Lou</li><li>2012-06-07 15:05:19</li><li>Start at 5348</li></ul></td></tr><tr class="even"><td class=""><ul><li>Lou</li><li>2012-06-07 14:15:19</li><li>CORRECTION:  Start at 5346</li></ul></td></tr></tbody></table></body>'''
