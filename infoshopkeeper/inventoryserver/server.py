import cherrypy
import uuid

from Cheetah.Template import Template
from simplejson import JSONEncoder
import turbojson

from sqlobject.sqlbuilder import *

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
encoder = JSONEncoder(ensure_ascii=False)

def jsonify_tool_callback(*args, **kwargs):
    response = cherrypy.response
    response.headers['Content-Type'] = 'application/json'
    response.body = turbojson.jsonify.encode(response.body)  #encoder.iterencode(response.body)

cherrypy.tools.jsonify = cherrypy.Tool('before_finalize', jsonify_tool_callback, priority=30)

class Noteboard:
    def __init__(self):
        self._notestemplate = NotesTemplate();
        
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
    
    @cherrypy.expose
    def build_cart(self, **args):
        return self._carttemplate.respond()
        
    @cherrypy.expose
    def add_item_to_cart(self, **kwargs):
        import sys
        print>>sys.stderr, "FUCK OFF"
        for arg in kwargs:
            print>>sys.stderr, arg
        cart={}
        if cherrypy.session.has_key('cart'):
            cart = cherrypy.session.pop('cart')
        else:
            cart['uuid']=uuid.uuid1().hex
        if not cart.has_key('items'):
            cart['items']=[]
        cart['items'].append(item)
        cherrypy.session['cart']=cart
        cherrypy.session.save()

    @cherrypy.tools.jsonify()
    @cherrypy.expose
    def get_cart(self):
        return cherrypy.session.get('cart')
        
    
    @cherrypy.expose
    def select_item_search(self, title="",sortby="booktitle",isbn="",distributor="",owner="",publisher="",author="",category="",out_of_stock='no',stock_less_than="",stock_more_than="",sold_more_than="", begin_date="",end_date="", tag="",kind="",location=""):
        self._chooseitemtemplate.empty=True
        self._chooseitemtemplate.title=title
        self._chooseitemtemplate.isbn=isbn
        self._chooseitemtemplate.author=author
        self._chooseitemtemplate.category=category
        self._chooseitemtemplate.distributor=distributor
        self._chooseitemtemplate.owner=owner
        self._chooseitemtemplate.publisher=publisher
        self._chooseitemtemplate.out_of_stock=out_of_stock
        self._chooseitemtemplate.stock_less_than=stock_less_than
        self._chooseitemtemplate.stock_more_than=stock_more_than
        self._chooseitemtemplate.sold_more_than=sold_more_than
        self._chooseitemtemplate.begin_date=begin_date
        self._chooseitemtemplate.end_date=end_date
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

        self._chooseitemtemplate.titles=titles
        return self._chooseitemtemplate.respond()
    
    @cherrypy.expose
    @cherrypy.tools.jsonify()
    def get_item_by_isbn(self, **kwargs):
        if kwargs['isbn']:
            isbn=kwargs['isbn']
        converted_isbn=isbn.strip('\'\"')
        if (isbn.replace(' ','').__len__()==13):
            converted_isbn=upc2isbn(isbn.replace(' ',''))
        t=Title.selectBy(isbn=converted_isbn)
        print t
        print list(t)
        if list(t):
            b=Book.selectBy(titleID=t[0].id).filter(Book.q.status=='STOCK').limit(1)
            print b
            print list(b)
        if list(t) and list(b):
            return {'title':list(t)[0], 'book':list(b)[0]}
        else:
            return {}

        
class Admin:
    def __init__(self):
        self._kindedittemplate = KindEditTemplate()
        self._kindlisttemplate = KindListTemplate()
        self._locationedittemplate = LocationEditTemplate()
        self._locationlisttemplate = LocationListTemplate()
        
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
        self._add_to_inventory_template=AddToInventoryTemplate()
    
        self.inventory=inventory.inventory()
        self.conn=db.connect()

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
    
    def add_to_inventory(self, isbn="", quantity=1, title="", listprice=0.0, ourprice=0.0, authors="", publisher="", categories="", distributor="", location="", owner=etc.default_owner, status="STOCK", tag="", kind=etc.default_kind, type='', known_title=False):
        self.common()
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
    def add_item_to_inventory(self, *args, **kwargs):
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
    def search_isbn(self, isbn=''):
        self.common()
        data=self.inventory.lookup_by_isbn(isbn)
        print "data is"
        print data
        return data
    add_to_inventory.search_isbn=search_isbn
    
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
    
    def search(self,title="",sortby="booktitle",isbn="",distributor="",owner="",publisher="",author="",category="",out_of_stock='no',stock_less_than="",stock_more_than="",sold_more_than="", begin_date="",end_date="", tag="",kind="",location=""):
        cherrypy.session['lastsearch']=False
        self.common()
        cherrypy.session['lastsearch']=cherrypy.url()
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
        return  self._searchtemplate.respond()            
            #~ if len(fields_used)>0 or out_of_stock=="yes":
            #~ self._searchtemplate.empty=False
            #~ if len(author)>0:
                #~ titles=Title.select("""
                #~ title.kind_id = '%s' AND
                #~ title.booktitle LIKE '%%%s%%' AND
                #~ title.publisher LIKE '%%%s%%' AND
                #~ title.tag LIKE '%%%s%%' AND
                #~ book.title_id=title.id AND book.distributor LIKE '%%%s%%' AND
        #~ book.sold_when > '%s' AND book.sold_when < '%s' AND
                #~ book.owner LIKE '%%%s%%'AND
                #~ author_title.title_id=title.id AND
        #~ author_title.author_id AND
        #~ author_title.author_id=author.id
        #~ AND author.author_name LIKE '%%%s%%'        
                #~ """ % (escape_string(the_kind),escape_string(title),escape_string(publisher),escape_string(tag),escape_string(distributor),escape_string(begin_date),escape_string(end_date),escape_string(owner),escape_string(author)),orderBy=sortby,clauseTables=['book','author','author_title'],distinct=True)

            #~ else:
                #~ if len(category)>0:
                    #~ titles=Title.select("""
                    #~ title.kind_id = '%s' AND
                    #~ title.booktitle LIKE '%%%s%%' AND
                    #~ title.publisher LIKE '%%%s%%' AND
                    #~ title.tag LIKE '%%%s%%' AND
                    #~ book.title_id=title.id AND book.distributor LIKE '%%%s%%' AND
                    #~ book.owner LIKE '%%%s%%' AND
                    #~ category.title_id=title.id AND category.category_name LIKE '%%%s%%'        
                #~ """ % (escape_string(the_kind),escape_string(title),escape_string(publisher),escape_string(tag),escape_string(distributor),escape_string(owner),escape_string(category)),orderBy=sortby,clauseTables=['book','category'],distinct=True)
                #~ else:
                
                    #~ # do a less complicated query
                    #~ titles=Title.select("""
                    #~ title.kind_id = '%s' AND
                    #~ title.booktitle LIKE '%%%s%%' AND
                    #~ title.publisher LIKE '%%%s%%' AND
                    #~ title.tag LIKE '%%%s%%' AND
                    #~ book.title_id=title.id AND book.distributor LIKE '%%%s%%'
                    #~ AND book.owner LIKE '%%%s%%'         
                    #~ """ % (escape_string(the_kind),escape_string(title),escape_string(publisher),escape_string(tag),escape_string(distributor),escape_string(owner)),orderBy=sortby,clauseTables=['book'],distinct=True)
                
            #~ if out_of_stock == 'yes':
                #~ titles = [t for t in titles if t.copies_in_status("STOCK") == 0]

            #~ if stock_less_than != "":
                #~ titles = [t for t in titles if t.copies_in_status("STOCK") <= int(stock_less_than)]

            #~ if stock_more_than != "":
                #~ titles = [t for t in titles if t.copies_in_status("STOCK") >= int(stock_more_than)]
                        
            #~ if sold_more_than != "":
                #~ titles = [t for t in titles if t.copies_in_status("SOLD") >= int(sold_more_than)]
            

    
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

        

    def reports(self,**args):
        self.common()
        self._reportlisttemplate.reports=[r.metadata for r in self.reportlist]
        return  self._reportlisttemplate.respond()

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




    transactions.exposed=True
    reports.exposed=True    
    report.exposed=True
    index.exposed = True
    search.exposed = True
    addtocart.exposed = True
    checkout.exposed = True
    bookedit.exposed = True
    authoredit.exposed = True
    categoryedit.exposed = True
    titleedit.exposed = True
    titlelist.exposed = True
    add_to_inventory.exposed = True



