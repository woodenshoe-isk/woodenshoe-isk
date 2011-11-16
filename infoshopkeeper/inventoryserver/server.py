#!/usr/bin/python
# coding: UTF-8
import cherrypy
import uuid
import sys

from mx.DateTime import now

from Cheetah.Template import Template
from simplejson import JSONEncoder
import turbojson
import json
from sqlobject.sqlbuilder import *


class MenuData:
    menuData={}
   
    @classmethod
    def getMenuData(cls):
        return [MenuData.menuData[key] for key in sorted(MenuData.menuData.keys())] 
    
    @classmethod
    def setMenuData(cls, dictionaryOfMenuLists):
        MenuData.menuData.update(dictionaryOfMenuLists)
     


from components import db
from components import inventory
from objects.title import Title
from objects.book import Book
from objects.author import Author
from objects.category import Category
from objects.kind import Kind
from objects.location import Location
from objects.transaction import Transaction
from objects.notes import Notes
from IndexTemplate import IndexTemplate
from SearchTemplate import SearchTemplate
from BookEditTemplate import BookEditTemplate
from TitleEditTemplate import TitleEditTemplate
from TitleListTemplate import TitleListTemplate
from AuthorEditTemplate import AuthorEditTemplate
from CategoryEditTemplate import CategoryEditTemplate
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
from AddToInventoryTemplate import AddToInventoryTemplate
from config import configuration
from upc import upc2isbn

import etc

cfg = configuration()

from MySQLdb import escape_string

import string
import re

import os.path
current_dir = os.path.dirname(os.path.abspath(__file__))

turbojson.jsonify._instance=turbojson.jsonify.GenericJSON(ensure_ascii=False)
def jsonify_tool_callback(*args, **kwargs):
    print>>sys.stderr, "in jsonify"
    cherrypy.response.headers['Content-type'] = 'application/json; charset=utf-8'
    body=turbojson.jsonify.encode(cherrypy.response.body).encode('utf-8')
    print>>sys.stderr, "body changed ", body
    cherrypy.response.headers['Content-length']=len(body)
    cherrypy.response.body=body
cherrypy.tools.jsonify = cherrypy.Tool('before_finalize', jsonify_tool_callback, priority=30)

class Noteboard:
    def __init__(self):
        self._notestemplate = NotesTemplate()
        self.menudata=MenuData
        MenuData.setMenuData({'5':('Notes', '/notes/noteboard', [])}) 
        
    @cherrypy.expose
    def noteboard(self):
        return self._notestemplate.respond()
    
    @cherrypy.expose
    @cherrypy.tools.jsonify()
    def get_notes(self, **kwargs):
        notes=[['<ul><li>%s</li><li>%s</li><li>%s</li></ul>' % (n.author, n.whenEntered, n.message)] for n in Notes.select().orderBy('-id')]
        return notes
        
    
    @cherrypy.expose
    def post_note(self, author='', message='', **kwargs):
        if kwargs:
            print "kwargs are ", kwargs
        if author:
            if message:
                print "author & message are ", author, " ", message
                Notes(author=author,  message=message)
                return self._notestemplate.respond()
        if kwargs['author']:
            if kwargs['message']:
                print "using kwargs to add note"
                Notes(author=kwargs['author'], message=kwargs['message'])
   
class Register:
    def __init__(self):
        self._carttemplate = CartTemplate2()
        self._chooseitemtemplate = ChooseItemTemplate()
        self.menudata=MenuData
        MenuData.setMenuData( {'1': ('Remove Items from Inventory', '/register/build_cart', []) })
    
    @cherrypy.expose
    def build_cart(self, **args):
        self._carttemplate.session_data=cherrypy.session.get('cart')
        print>>sys.stderr, "BuildCart: ", self._carttemplate.session_data
        return self._carttemplate.respond()
        
    @cherrypy.expose
    def add_item_to_cart(self, **args):
        import sys
        print>>sys.stderr, "IN add_item_to_cart     ARGS ARE"
        print>>sys.stderr, args, repr(args)
        cart={}
        print>>sys.stderr, "SESSION IS: ", cherrypy.session
        if cherrypy.session.has_key('cart'):
            print>>sys.stderr, "CART EXISTS"         
            cart = cherrypy.session.pop('cart')
        else:
            print>>sys.stderr, "MAKE CART" 
            cart['uuid']=uuid.uuid1().hex
        if not cart.has_key('items'):
            print>>sys.stderr, "MAKE ITEM ARRAY"
            cart['items']=[]
        
        if args.has_key('titleid'):
            print>>sys.stderr, "in title block"
            print>>sys.stderr, args['titleid']
            t1=Title.selectBy(id=args['titleid'] )[0]
            print>>sys.stderr, t1
            b1=Book.selectBy(titleID=t1.id).filter(Book.q.status=='STOCK')[0]
            print>>sys.stderr, b1
            cart['items'].append({u'department':t1.kind.kindName.title(), u'booktitle':t1.booktitle, u'isbn':t1.isbn, u'titleID':t1.id, u'bookID':b1.id, u'ourprice':b1.ourprice})
        elif args.has_key('item'):
            print>>sys.stderr, "in item block", args['item'], type(args['item']), json.loads(args['item'])
            cart['items'].append(json.loads(args['item']))
        
        cherrypy.session['cart']=cart
        cherrypy.session.save()
        print>>sys.stderr, "CART NOW IS: ", cherrypy.session.get('cart');
        print>>sys.stderr, "SESSION NOW IS: ", cherrypy.session
    
    @cherrypy.expose
    def remove_item_from_cart(self, **args):
        print>>sys.stderr, "args are ", args
        print>>sys.stderr, type(int(args['index']))
        print>>sys.stderr, int(args['index'])        
        item_index=int(args['index'])
        cart={}
        if cherrypy.session.has_key('cart'):
            cart=cherrypy.session['cart']
            print>>sys.stderr, cart, cart['items'], cart['items'][item_index]
        if cart.has_key('items'):
            print>>sys.stderr, "has items"
            cart['items'].pop(item_index)
            print>>sys.stderr, cart
        cherrypy.session['cart']=cart
        cherrypy.session.save()

    @cherrypy.expose
    def void_cart(self):
        cart={}
        if cherrypy.session.has_key('cart'):
            cart=cherrypy.session['cart']
        if cart.has_key('items'):
            cart['items']=[]
        cherrypy.session['cart']=cart
        cherrypy.session.save()
                
    @cherrypy.expose
    def check_out(self):
        cart={}
        print>>sys.stderr, "in checkout"
        if cherrypy.session.has_key('cart'):
            cart=cherrypy.session['cart']
            if cart.has_key('items'):
                shouldRaiseException=False
                for item in cart['items']:
                    if item['bookID']:
                        try:
                            Book.selectBy(id=item['bookID'])[0].set(status='SOLD', sold_when=now())
                            infostring = "'[] " + item['department']
                            if item.has_key('booktitle'):
                                infostring=infostring + ": " +item['booktitle']
                            Transaction(action='SALE', date=now(), info=infostring, owner=None, cashier=None, schedule=None, amount=item['ourprice'])
                            cart['items'].remove(item)
                        except Exception as err:
                            print>>sys.stderr, err
                            shouldRaiseException=True
                    else:
                        infostring = "'[] " + item['department']
                        if item.haskey('booktitle'):
                            infostring=infostring + ": " +item['booktitle']
                        Transaction(action='SALE', date=now(), info=infostring, owner=None, cashier=None, amount=item['ourprice'])
                        cart['items'].remove(item)
            print>>sys.stderr, shouldRaiseException
            if cart['items'].__len__()==0:
                cherrypy.session['cart']={}
            else:
                cherrypy.session['cart']=cart
            cherrypy.session.save()
            if shouldRaiseException:
                raise SQLObjectNotFound
                                
         
    @cherrypy.tools.jsonify()
    @cherrypy.expose
    def get_cart(self):
        return cherrypy.session.get('cart')
    
    @cherrypy.expose
    def select_item_search(self, title="",sortby="booktitle",isbn="",distributor="",owner="",publisher="",author="",category="", tag="",kind="",location=""):
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
        self._chooseitemtemplate.kinds=list(Kind.select())
        self._chooseitemtemplate.kind=kind
        the_kind=kind
        if type(the_kind) == type([]):
            the_kind=the_kind[0]
        self._chooseitemtemplate.table_is_form=True
        
        titles=[]
        fields=[title,author,category,distributor,owner,isbn,publisher,tag,kind]
        fields_used = [f for f in fields if f != ""]
        
        where_clause_list = ["book.title_id=title.id", "author_title.title_id=title.id", "author_title.author_id=author.id", "category.title_id=title.id"]
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
            converted_isbn=upc2isbn(isbn)
            where_clause_list.append("title.isbn RLIKE '%s'" % escape_string(converted_isbn))
        if owner:
            where_clause_list.append("book.owner RLIKE '%s'" % escape_string(owner.strip()))
        if distributor:
            where_clause_list.append("book.distributor RLIKE '%s'" % escape_string(distributor.strip()))
        if author:
            where_clause_list.append("author.author_name RLIKE '%s'" % escape_string(author.strip()))
        if category:
            where_clause_list.append("category.category_name RLIKE '%s'" % escape_string(category.strip()))
        where_clause=' AND '.join(where_clause_list)
        titles=[]
        if len(fields_used)>0:
            titles=Title.select( where_clause,orderBy=sortby,clauseTables=['book','author','author_title', 'category'],distinct=True)
        titles = [t for t in titles if t.copies_in_status("STOCK") >= 1]
        
        self._chooseitemtemplate.titles=titles
        return self._chooseitemtemplate.respond()
    
    @cherrypy.expose
    @cherrypy.tools.jsonify()
    def get_item_by_isbn(self, **kwargs):
        print>>sys.stderr, kwargs
        if kwargs['isbn']:
            isbn=kwargs['isbn']
            print>>sys.stderr, isbn
        isbn=isbn.strip('\'\"')
        print>>sys.stderr, isbn
        if (isbn.replace(' ','').__len__()==13):
            isbn=upc2isbn(isbn.replace(' ',''))
        t=Title.selectBy(isbn=isbn)
        b=[]
        if list(t):
            for t1 in Title.selectBy(isbn=isbn):
                for b1 in Book.selectBy(titleID=t1.id).filter(Book.q.status=='STOCK'):
                    b.append(b1)
            b.sort(key=lambda x: x.inventoried_when)
            if b:
                return [{'titleID':b[0].title.id, 'booktitle':b[0].title.booktitle, 'isbn':b[0].title.isbn, 'bookID':b[0].id, 'ourprice':b[0].ourprice}]
            else:
                return []
        else:
            return []

        
class Admin:
    def __init__(self):
        self._kindedittemplate = KindEditTemplate()
        self._kindlisttemplate = KindListTemplate()
        self._locationedittemplate = LocationEditTemplate()
        self._locationlisttemplate = LocationListTemplate()
        self._add_to_inventory_template=AddToInventoryTemplate()
    
        self.inventory=inventory.inventory()
        
        MenuData.setMenuData({'3': ('Add to Inventory', '/admin/add_to_inventory', [])})
        MenuData.setMenuData({'6':('Admin', '', [  ('Edit Item Kinds', '/admin/kindlist', []),
                                                   ('Edit Item Locations', '/admin/locationlist', []),
                                                 ])})
                                                 
    @cherrypy.expose
    def kindedit(self,**args):
        if ('kindName' in args.keys()):
            self._kindedittemplate.kind=Kind.form_to_object(Kind,args)
            return self.kindlist()
        else:
            self._kindedittemplate.kind=Kind.form_to_object(Kind,args)
            return self._kindedittemplate.respond()
    
    @cherrypy.expose    
    def kindlist(self,**args):
        self._kindlisttemplate.kinds=list(Kind.select())
        return self._kindlisttemplate.respond()
    
    @cherrypy.expose
    def locationedit(self,**args):
        if ('locationName' in args.keys()):
            self._locationedittemplate.location=Location.form_to_object(Location,args)
            return self.locationlist()
        else:
            self._locationedittemplate.location=Location.form_to_object(Location,args)
            return self._locationedittemplate.respond()
            
    @cherrypy.expose
    def locationlist(self,**args):
        self._locationlisttemplate.locations=list(Location.select(orderBy="location_name"))
        return self._locationlisttemplate.respond()

    @cherrypy.expose
    def add_to_inventory(self, isbn="", quantity=1, title="", listprice='0.0', ourprice='0.0', authors="", publisher="", categories="", distributor="", location="", owner=etc.default_owner, status="STOCK", tag="", kind=etc.default_kind, type='', known_title=False):
        self._add_to_inventory_template.isbn=isbn
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
        
        conn=Title._connection
        query=Select( Title.q.type, groupBy=Title.q.type)
        results=conn.queryAll( conn.sqlrepr(query))
        typelist=[t[0] for t in results] 
        self._add_to_inventory_template.formats=typelist
        self._add_to_inventory_template.format=type
        self._add_to_inventory_template.known_title=known_title

        return self._add_to_inventory_template.respond()

    @cherrypy.expose
    def add_item_to_inventory(self, **kwargs):
        print "kwargs are:" 
        print kwargs
        kwargs['listprice']=float(kwargs['listprice'].replace('$', ''))
        kwargs['ourprice']=float(kwargs['ourprice'].replace('$', ''))
        kwargs['authors']=kwargs['authors'].split(',')
        kwargs['categories'] = kwargs['categories'].split(',')
        if kwargs['known_title'] == 'false':
            kwargs['known_title']=False
        else:
            kwargs['known_title'] = list(Title.selectBy(isbn=kwargs['isbn']).orderBy("id").limit(1))[0]
        print kwargs
        self.inventory.addToInventory(**kwargs)

    @cherrypy.expose
    @cherrypy.tools.jsonify()
    def search_isbn(self, **args):
        print>>sys.stderr, "in search_isbn"
        data=self.inventory.lookup_by_isbn(args['isbn'])
        print>>sys.stderr, "data is"
        print>>sys.stderr, data
        return [data]
    add_to_inventory.search_isbn=search_isbn
            
class InventoryServer:
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
 
        self.reportlist=[getattr(__import__('reports.'+x,globals(),{},[1]),x) for x in cfg.get("reports")]

        
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
    
        self.inventory=inventory.inventory()
        self.conn=db.connect()
        
        MenuData.setMenuData({'2': ('Search the Inventory', '/search', [])})
        MenuData.setMenuData({'4': ('Reports', '/reports',
                                        [(i.metadata['name'], '/report?reportname=' + i.metadata['action'], []) for i in self.reportlist])})
        
    @cherrypy.expose
    def test(self):
        raise Exception("Test exception")
        
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
        
    @cherrypy.expose
    def index(self,**args):
        self.common()
        cherrypy.session['c'] = cherrypy.session.get('c',0)+1
        print   cherrypy.session['c']
        return self._indextemplate.respond()
    
    @cherrypy.expose
    def bookedit(self,**args):
        self.common()
        self._bookedittemplate.book=Book.form_to_object(Book,args)
        return self._bookedittemplate.respond()

    @cherrypy.expose
    def authoredit(self,**args):
        self.common()
        self._authoredittemplate.author=Author.form_to_object(Author,args)
        return self._authoredittemplate.respond()
    
    @cherrypy.expose
    def categoryedit(self,**args):
        self.common()
        self._categoryedittemplate.category=Category.form_to_object(Category,args)
        return self._categoryedittemplate.respond()
    
    @cherrypy.expose
    def titleedit(self,**args):
        self.common()
        self._titleedittemplate.title=Title.form_to_object(Title,args)
        return self._titleedittemplate.respond()

    @cherrypy.expose
    def titlelist(self,**args):
        self.common()
        self._titlelisttemplate.titles=[]
        try:
            if (type(args['titles']) is types.UnicodeType) or (type(args['titles']) is types.StringType):
                print int(args['titles'])
                self._titlelisttemplate.titles.append(Title.get(int(args['titles'])))
                print self._titlelisttemplate.titles
            else:
                for id in args['titles']:
                    self._titlelisttemplate.titles.append(Title.get(int(id)))
                print self._titlelisttemplate.titles
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

    @cherrypy.expose
    def checkout(self,**args):
        self.common()
        self._checkouttemplate.status_from=args.get("status_from","STOCK")
        self._checkouttemplate.status_to=args.get("status_to","RETURNED")
        self._checkouttemplate.schedules = [("list price",1)]+cfg.get("multiple_prices")

        
        if "change" in args:
            return self.addtocart(**args)
        if "finalize" in args:
            schedule_name=args["schedule"]
            print cfg
            print cfg.get("multiple_prices")
            schedule=[x for x in cfg.get("multiple_prices")+[("list price",1)] if x[0]==schedule_name] 
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
                    print str(e)

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
    
    @cherrypy.expose
    def search(self,title="",sortby="booktitle",isbn="",distributor="",owner="",publisher="",author="",category="",out_of_stock='no',stock_less_than="",stock_more_than="",sold_more_than="", begin_date="",end_date="", tag="",kind="",location="", formatType=""):
        cherrypy.session['lastsearch']=False
        self.common()
        cherrypy.session['lastsearch']=cherrypy.url()
        print>>sys.stderr, "In SEarch"

        self._searchtemplate.empty=True
        self._searchtemplate.title=title
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
        self._searchtemplate.begin_date=begin_date
        self._searchtemplate.end_date=end_date
        self._searchtemplate.tag=tag
        self._searchtemplate.locations=list(Location.select(orderBy="location_name"))
        self._searchtemplate.location=location
        the_location=location
        if type(the_location)==type([]):
            the_location=the_location[0]

        conn=Title._connection
        query=Select( Title.q.type, groupBy=Title.q.type)
        results=conn.queryAll( conn.sqlrepr(query))
        formatTypelist=[t[0] for t in results]
        print>>sys.stderr, formatTypelist, formatType
        self._searchtemplate.formats=formatTypelist
        self._searchtemplate.formatType=formatType
        
        self._searchtemplate.kinds=list(Kind.select())
        self._searchtemplate.kind=kind
        the_kind=kind
        if type(the_kind) == type([]):
            the_kind=the_kind[0]
        
        titles=[]
        fields=[title,author,category,distributor,owner,isbn,publisher,stock_less_than,stock_more_than,sold_more_than,begin_date,end_date,tag,kind]
        fields_used = [f for f in fields if f != ""]
        
        where_clause_list = ["book.title_id=title.id", "author_title.title_id=title.id", "author_title.author_id=author.id", "category.title_id=title.id"]
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
            converted_isbn=upc2isbn(isbn)
            where_clause_list.append("title.isbn RLIKE '%s'" % escape_string(converted_isbn))
        if formatType:
            print>>sys.stderr, formatType, formatType.strip(), escape_string(formatType.strip())
            where_clause_list.append("title.type RLIKE '%s'" % escape_string(formatType.strip()))
        if owner:
            where_clause_list.append("book.owner RLIKE '%s'" % escape_string(owner.strip()))
        if distributor:
            where_clause_list.append("book.distributor RLIKE '%s'" % escape_string(distributor.strip()))
        if begin_date:
            where_clause_list.append("book.sold_when >= '%s'" % escape_string(begin_date))
        if end_date:
            where_clause_list.append("book.sold_when < '%s'" % escape_string(end_date))
        if author:
            where_clause_list.append("author.author_name RLIKE '%s'" % escape_string(author.strip()))
        if category:
            where_clause_list.append("category.category_name RLIKE '%s'" % escape_string(category.strip()))
        where_clause=' AND '.join(where_clause_list)
        print>>sys.stderr, where_clause

        titles=[]
        if len(fields_used)>0 or out_of_stock=="yes":
            titles=Title.select( where_clause,orderBy=sortby,clauseTables=['book','author','author_title', 'category'],distinct=True)
        if out_of_stock == 'yes':
                    titles = [t for t in titles if t.copies_in_status("STOCK") == 0]
    
        if stock_less_than != "":
            titles = [t for t in titles if t.copies_in_status("STOCK") <= int(stock_less_than)]
    
        if stock_more_than != "":
            titles = [t for t in titles if t.copies_in_status("STOCK") >= int(stock_more_than)]
            
        if sold_more_than != "":
            titles = [t for t in titles if t.copies_in_status("SOLD") >= int(sold_more_than)]

        self._searchtemplate.titles=titles
        print>>sys.stderr, titles
        print>>sys.stderr, "GOT TO END"
        return  self._searchtemplate.respond()            

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

        

    @cherrypy.expose
    def reports(self,**args):
        self.common()
        self._reportlisttemplate.reports=[r.metadata for r in self.reportlist]
        return  self._reportlisttemplate.respond()

    @cherrypy.expose
    def report(self,**args):
        self.common()
        the_report=[r for r in self.reportlist if r.metadata['action']==args['reportname']][0](args)
        self._reporttemplate.report=the_report
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
        else:
            self._reporttemplate.do_query=False
            
        return  self._reporttemplate.respond()

