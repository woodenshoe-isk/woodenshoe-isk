import unittest
import sys
import tidylib
import random
import webtest
import json
import mx

from objects.author import Author
from objects.book import Book
from objects.category import Category
from objects.title import Title
from objects.transaction import Transaction

from inventoryserver.server import Noteboard
from inventoryserver.server import Register
from inventoryserver.server import Admin
from inventoryserver.server import InventoryServer

from tools.run_sql_select import run_sql_select

from myapp_local import application

#class MenuData:
    #def getMenuData(cls):
    #def setMenuData(cls, dictionaryOfMenuLists):
#def jsonify_tool_callback(*args, **kwargs):

#class Noteboard:
    #def noteboard(self):
    #def get_notes(self, **kwargs):
    #def post_note(self, author='', message='', **kwargs):
class Test_Noteboard(unittest.TestCase):
    def setUp(self):
        try:
            self._my_class=Noteboard()
        except Exception as excp:
            pass
    
    def test_noteboard_class_instantiates(self):
        self.assertIsInstance(self._my_class, Noteboard, "Could not instantiate Noteboard")
    
    def test_noteboard_returns_page(self):
        code, error=tidylib.tidy_document(self._my_class.noteboard(), options={'show-errors':1,'show-warnings':0})
        self.assertFalse(error, "/notes/noteboard does not return valid html page")

    def test_get_notes(self):
        result=self._my_class.get_notes()
        self.assertIsInstance( result, type([]), "/notes/get_notes does not return array")

    def test_post_note(self):
        code, error=tidylib.tidy_document(self._my_class.post_note(**{'author':'test', 'message':'test'}), options={'show-errors':1,'show-warnings':0})
        self.assertFalse(error, "/notes/post_note does not return valid html page")

 #class Register:
    #def __init__(self):
    #def build_cart(self, **args):
    #def add_item_to_cart(self, **args):
    #def remove_item_from_cart(self, **args):
    #def void_cart(self):
    #def check_out(self):
    #def get_cart(self):
    #def select_item_search(self, title="",sortby="booktitle",isbn="",distributor="",owner="",publisher="",author="",category="", tag="",kind="",location=""):
    #def get_item_by_isbn(self, **kwargs):
class Test_Register(unittest.TestCase ):
    def setUp(self):
        try:
            self._my_class=Register()
        except Exception as excp:
            pass
        try:
            self._my_app=webtest.TestApp(application)
            #print self._my_app
        except Exception as excp:
            #print excp
            sys.exit(0)

    def test_register_class_instantiates(self):
        self.assertIsInstance(self._my_class, Register, "Register class did not instiate")
    
    @unittest.expectedFailure
    def test_build_cart_unit(self):
        code, error=tidylib.tidy_document(self._my_class.build_cart(), options={'show-errors':1,'show-warnings':0})
        self.assertFalse(error, "method build_cart does not return valid html page")
        
    def test_build_cart_functional(self):
        response=self._my_app.get('/register/build_cart')
        code, error=tidylib.tidy_document(response.body, options={'show-errors':1, 'show-warnings':0})
        self.assertFalse(error, '/register/build_cart did not return functional html')

    def test_get_cart_empty(self):
        reply=self._my_app.get('/register/get_cart')
        self.assertNotEqual(reply.json, [], "couldn't get empty cart")

    @unittest.expectedFailure
    def test_add_item_to_cart_unit(self):
        random_item=random.sample(list(Book.selectBy(status='STOCK')), 1)[0]
        args={'item':{"department":"Book","isInventoried":"True","isTaxable":"True","booktitle":random_item.title.booktitle,"isbn":random_item.title.isbn,"bookID":random_item.id,"titleID":random_item.titleID,"ourprice":random_item.ourprice}}
        result=self._my_class.add_item_to_cart(**args)
        self.assertTrue(result, '/register/add_item_to_cart returned error in unittest')

    def test_add_item_to_cart_functional(self):
        random_item=random.sample(list(Book.selectBy(status='STOCK')), 1)[0]
        item={"department":"Book","isInventoried":"True","isTaxable":"True","booktitle":random_item.title.booktitle,"isbn":random_item.title.isbn,"bookID":random_item.id,"titleID":random_item.titleID,"ourprice":random_item.ourprice}
        result=self._my_app.post('/register/add_item_to_cart', {'item':json.dumps(item)})
        confirm=self._my_app.get('/register/get_cart')
        print "confirm is", confirm
        print "test_add_inventoried", confirm.json[0]['items'][0]
        confirm=confirm.json[0]['items'][0]
        self.assertEqual(item, confirm, '/register/add_item_to_cart returned error in function test')

    def test_remove_item_from_cart_functional(self):
        random_item=random.sample(list(Book.selectBy(status='STOCK')), 1)[0]
        item={"department":"Book","isInventoried":"True","isTaxable":"True","booktitle":random_item.title.booktitle,"isbn":random_item.title.isbn,"bookID":random_item.id,"titleID":random_item.titleID,"ourprice":random_item.ourprice}
        self._my_app.post('/register/add_item_to_cart', {'item':json.dumps(item)})
        self._my_app.post('/register/remove_item_from_cart', {'index':0})
        confirm=self._my_app.get('/register/get_cart').json[0]['items']
        self.assertEqual(confirm, [], "/register/remove_item_from_cart failed.")

    def test_void_cart(self):
        random_item_list=random.sample(list(Book.selectBy(status='STOCK')), 3)
        for random_item in random_item_list:
            item={"department":"Book","isInventoried":"True","isTaxable":"True","booktitle":random_item.title.booktitle,"isbn":random_item.title.isbn,"bookID":random_item.id,"titleID":random_item.titleID,"ourprice":random_item.ourprice}
            self._my_app.post('/register/add_item_to_cart', {'item':json.dumps(item)})
        self._my_app.post('/register/void_cart')
        confirm=self._my_app.get('/register/get_cart').json[0]
        self.assertEqual(confirm, {}, '/register/void_cart failed to destroy cart')
    
    def test_check_out_zeros_cart(self):
        random_item=random.sample(list(Book.selectBy(status='STOCK')), 1)[0]
        item={"department":"Book","isInventoried":"True","isTaxable":"True","booktitle":random_item.title.booktitle,"isbn":random_item.title.isbn,"bookID":random_item.id,"titleID":random_item.titleID,"ourprice":random_item.ourprice}
        self._my_app.post('/register/add_item_to_cart', {'item':json.dumps(item)})
        self._my_app.post('/register/check_out')
        confirm=self._my_app.get('/register/get_cart').json[0]
        self.assertEqual(confirm, {}, '/register/checkout failed to destroy cart')

    def test_check_out_sells_book(self):
        random_item=random.sample(list(Book.selectBy(status='STOCK')), 1)[0]
        item={"department":"Book","isInventoried":"True","isTaxable":"True","booktitle":random_item.title.booktitle,"isbn":random_item.title.isbn,"bookID":random_item.id,"titleID":random_item.titleID,"ourprice":random_item.ourprice}
        self._my_app.post('/register/add_item_to_cart', {'item':json.dumps(item)})
        self._my_app.post('/register/check_out')
        confirm=random_item.status
        self.assertEqual(confirm, 'SOLD', '/register/checkout failed mark book \'SOLD\'')
        
    def test_check_out_records_transaction(self):
        random_item=random.sample(list(Book.selectBy(status='STOCK')), 1)[0]
        item={"department":"Book","isInventoried":"True","isTaxable":"True","booktitle":random_item.title.booktitle,"isbn":random_item.title.isbn,"bookID":random_item.id,"titleID":random_item.titleID,"ourprice":random_item.ourprice}
        self._my_app.post('/register/add_item_to_cart', {'item':json.dumps(item)})
        cart_id=self._my_app.get('/register/get_cart').json[0]['uuid']        
        self._my_app.post('/register/check_out')
        transaction=Transaction.selectBy(cartID=cart_id)
        #print transaction
        self.assertEqual('SOLD', 'SOLD', '/register/checkout failed mark book \'SOLD\'')

    def test_select_item_search(self):
        random_item=random.sample(list(Book.selectBy(status='STOCK')), 1)[0]
        code, error=tidylib.tidy_document(self._my_class.select_item_search(title=random_item.title.booktitle), options={'show-errors':1,'show-warnings':0})
        self.assertFalse(error, "/register/select_item_search does not return valid html page")

    def test_get_item_by_isbn_in_stock(self):
        random_item=random.sample(list(Book.selectBy(status='STOCK')), 1)[0]
        result=self._my_class.get_item_by_isbn(**{'isbn':random_item.title.isbn})
        #print "isbn_stock", random_item, result
        self.assertTrue(result, "/register/get_item_by_isbn does not return item when it should")

    def test_get_item_by_isbn_out_of_stock(self):
        #lookign for a title where none of its copies are in stock
        query_string='''
            SELECT * 
            FROM title t2 
            JOIN book b2 
              ON b2.title_id=t2.id 
            JOIN (SELECT 
                    t1.isbn 
                  FROM title t1  
                  JOIN book b1 
                    ON t1.id=b1.title_id 
                 GROUP BY t1.isbn 
                HAVING COUNT(
                        CASE WHEN b1.status='STOCK' 
                        THEN 1 END) = 0 
                ORDER BY t1.booktitle) as subq1 
            ON t2.isbn=subq1.isbn'''
        results= run_sql_select( query_string )
        random_item= random.sample( results, 1 )[0]
        self.assertFalse(self._my_class.get_item_by_isbn(**{'isbn':random_item['isbn']}), "/register/get_item_by_isbn returns item when it shouldn't")

#class Admin:
    #def __init__(self):
    #def kindedit(self,**args):
    #def kindlist(self,**args):
    #def locationedit(self,**args):
    #def locationlist(self,**args):
    #def add_to_inventory(self, isbn="", quantity=1, title="", listprice='0.0', ourprice='0.0', authors="", publisher="", categories="", distributor="", location="", owner=etc.#default_owner, status="STOCK", tag="", kind=etc.#default_kind, type='', known_title=False):
    #def add_item_to_inventory(self, **kwargs):
    #def search_isbn(self, **args):
class Test_Admin(unittest.TestCase ):
    def setUp(self):
        try:
            self._my_class=Admin()
        except Exception as excp:
            pass
        try:
            self._my_app=webtest.TestApp(application)
        except:
            pass
        
    def test_admin_class_instantiates(self):
        self.assertIsInstance(self._my_class, Admin, "Admin class did not instantiate properly")
            
    def test_kindedit_unit(self):
        code, error=tidylib.tidy_document(self._my_class.kindedit(), options={'show-errors':1,'show-warnings':0})
        self.assertFalse(error, "method Admin.kindedit does not return valid html page")
        
    def test_kindedit_functional(self):
        response=self._my_app.get('/admin/kindedit')
        code, error=tidylib.tidy_document(response.body, options={'show-errors':1, 'show-warnings':0})
        self.assertFalse(error, '/admin/kindedit did not return valid html page')

    def test_kindlist_unit(self):
        code, error=tidylib.tidy_document(self._my_class.kindlist(), options={'show-errors':1,'show-warnings':0})
        self.assertFalse(error, "method Admin.kindlist does not return valid html page")
        
    def test_kindlist_functional(self):
        response=self._my_app.get('/admin/kindlist')
        code, error=tidylib.tidy_document(response.body, options={'show-errors':1, 'show-warnings':0})
        self.assertFalse(error, '/admin/kindlist did not return valid html page')
        
    def test_locationedit_unit(self):
        code, error=tidylib.tidy_document(self._my_class.locationedit(), options={'show-errors':1,'show-warnings':0})
        self.assertFalse(error, "method Admin.locationedit does not return valid html page")
        
    def test_locationedit_functional(self):
        response=self._my_app.get('/admin/locationedit')
        code, error=tidylib.tidy_document(response.body, options={'show-errors':1, 'show-warnings':0})
        self.assertFalse(error, '/admin/locationedit did not return valid html page')
        
    def test_locationlist_unit(self):
        code, error=tidylib.tidy_document(self._my_class.locationlist(), options={'show-errors':1,'show-warnings':0})
        self.assertFalse(error, "method Admin.locationlist does not return valid html page")
        
    def test_locationlist_functional(self):
        response=self._my_app.get('/admin/locationlist')
        code, error=tidylib.tidy_document(response.body, options={'show-errors':1, 'show-warnings':0})
        self.assertFalse(error, '/admin/locationlist did not return valid html page')
    
    def test_get_next_unused_local_isbn(self):
        isbn = self._my_class.get_next_unused_local_isbn() 
        self.assertRegexpMatches(isbn, '^199\d{10}$', "method get_next_unused_local_isbn doesn't return valid isbn")

    def test_add_to_inventory_unit(self):
        code, error=tidylib.tidy_document(self._my_class.add_to_inventory(), options={'show-errors':1,'show-warnings':0})
        self.assertFalse(error, "method Admin.add_to_inventory does not return valid html page")
        
    def test_add_to_inventory_functional(self):
        response=self._my_app.get('/admin/add_to_inventory')
        code, error=tidylib.tidy_document(response.body, options={'show-errors':1, 'show-warnings':0})
        self.assertFalse(error, '/admin/add_to_inventory did not return valid html page')
        
    def test_add_item_to_inventory_that_we_have_already_returns_object(self):
        random_item=random.sample(list(Book.selectBy(status='STOCK')), 1)[0]
        fakeargs=dict(title=random_item.title.booktitle, authors=random_item.title.authors_as_string(), publisher=random_item.title.publisher, distributor=random_item.distributor, owner='woodenshoe', listprice=random_item.listprice, ourprice=random_item.ourprice, isbn=random_item.title.isbn, categories=random_item.title.categories_as_string(), location=random_item.location, quantity=1, known_title=True, types=random_item.title.type, kind=random_item.title.kind.id, kind_name=random_item.title.kind.kindName)
        response=self._my_app.post('/admin/add_item_to_inventory', fakeargs)
        today=mx.DateTime.now().strftime('%Y-%m-%d')
        confirm=Book.selectBy(titleID=random_item.titleID).filter('inventoried_when=%s' % today)
        self.assertTrue(confirm, "test_add_item_to_inventory does not add item to inventory")
    
    def test_add_item_to_inventory_that_we_have_already_records_transaction(self):
        random_item=random.sample(list(Book.select()), 1)[0]
        fakeargs=dict(title=random_item.title.booktitle, authors=random_item.title.authors_as_string(), publisher=random_item.title.publisher, distributor=random_item.distributor, owner='woodenshoe', listprice=random_item.listprice, ourprice=random_item.ourprice, isbn=random_item.title.isbn, categories=random_item.title.categories_as_string(), location=random_item.location, quantity=1, known_title=True, types=random_item.title.type, kind=random_item.title.kind.id, kind_name=random_item.title.kind.kindName)
        response=self._my_app.post('/admin/add_item_to_inventory', fakeargs)
        nowish=mx.DateTime.now().strftime('%Y-%m-%d %H:%M:%S')
        confirm=Transaction.select('date > %s' % nowish).filter('info RLIKE %s' % random_item.title.booktitle)
        self.assertTrue(confirm, "test_add_item_to_inventory does not add item to inventory")
        
    def test_add_item_to_inventory_that_we_dont_have_returns_object(self):
        random_item=random.sample(list(Book.selectBy(status='STOCK')), 1)[0]
        fakeargs=dict(title=random_item.title.booktitle, authors=random_item.title.authors_as_string(), publisher=random_item.title.publisher, distributor=random_item.distributor, owner='woodenshoe', listprice=random_item.listprice, ourprice=random_item.ourprice, isbn=random_item.title.isbn, categories=random_item.title.categories_as_string(), location=random_item.location, quantity=1, known_title=True, types=random_item.title.type, kind=random_item.title.kind.id, kind_name=random_item.title.kind.kindName)
        response=self._my_app.post('/admin/add_item_to_inventory', fakeargs)
        today=mx.DateTime.now().strftime('%Y-%m-%d')
        confirm=Book.selectBy(titleID=random_item.titleID).filter('inventoried_when=%s' % today)
        self.assertTrue(confirm, "test_add_item_to_inventory does not add item to inventory")
    
    def test_add_item_to_inventory_that_we_dont_have_records_transaction(self):
        random_item=random.sample(list(Book.select()), 1)[0]
        fakeargs=dict(title=random_item.title.booktitle, authors=random_item.title.authors_as_string(), publisher=random_item.title.publisher, distributor=random_item.distributor, owner='woodenshoe', listprice=random_item.listprice, ourprice=random_item.ourprice, isbn=random_item.title.isbn, categories=random_item.title.categories_as_string(), location=random_item.location, quantity=1, known_title=True, types=random_item.title.type, kind=random_item.title.kind.id, kind_name=random_item.title.kind.kindName)
        response=self._my_app.post('/admin/add_item_to_inventory', fakeargs)
        nowish=mx.DateTime.now().strftime('%Y-%m-%d %H:%M:%S')
        confirm=Transaction.select('date > %s' % nowish).filter('info RLIKE %s' % random_item.title.booktitle)
        self.assertTrue(confirm, "test_add_item_to_inventory does not add item to inventory")
    
    def test_search_isbn_that_we_have_unit(self):
        random_item=random.sample(list(Title.select()), 1)[0]
        result=self._my_class.search_isbn(**{'isbn':random_item.isbn})[0]
        self.assertEqual(result['isbn'], random_item.isbn, "method search_isbn doesn't return proper item for isbn10")

    def test_search_isbn_that_we_have_functional(self):
        random_item=random.sample(list(Title.select()), 1)[0]
        response=self._my_app.get('/admin/search_isbn', {'isbn':random_item.isbn}).json[0]
        self.assertEqual(response['isbn'], random_item.isbn, "/admin/search_isbn doesn't return proper item for isbn10")

    def test_search_isbn_that_we_dont_have_unit(self):
        random_item=random.sample(list(Title.select()), 1)[0]
        result=self._my_class.search_isbn(**{'isbn':random_item.isbn})[0]
        print result
        self.assertEqual(result['isbn'], random_item.isbn, "method search_isbn doesn't return proper item for isbn10")

    def test_search_isbn_that_we_dont_have_functional(self):
        random_item=random.sample(list(Title.select()), 1)[0]
        response=self._my_app.get('/admin/search_isbn', {'isbn':random_item.isbn}).json[0]
        self.assertEqual(response['isbn'], random_item.isbn, "/admin/search_isbn doesn't return proper item for isbn10")

#class InventoryServer:
    #def __init__(self):
    #def test(self):
    #def loadUserByUsername(self, login):
    #def checkLoginAndPassword(self, login, password):
    #def common(self):
    #def index(self,**args):
    #def bookedit(self,**args):
    #def authoredit(self,**args):
    #def categoryedit(self,**args):
    #def titleedit(self,**args):
    #def titlelist(self,**args):
    #def checkout(self,**args):
    #def addtocart(self,**args):
    #def search(self,title="",sortby="booktitle",isbn="",distributor="",owner="",publisher="",author="",category="",out_of_stock='no',stock_less_than="",stock_more_than="",sold_more_than="", begin_date="",end_date="", tag="",kind="",location="", formatType=""):
    #def transactions(self,**args):
    #def reports(self,**args):
    #def report(self,**args):
class Test_InventoryServer(unittest.TestCase ):
    
    def setUp(self):
        try:
            self._my_class=InventoryServer()
        except Exception as excp:
            pass
        try:
            self._my_app=webtest.TestApp(application)
        except:
            pass

    @unittest.expectedFailure
    def test_index_unit(self):
        code, error=tidylib.tidy_document(self._my_class.index(), options={'show-errors':1,'show-warnings':0})
        self.assertFalse(error, "method InventoryServer.index does not return valid html page")
        
    def test_index_functional(self):
        response=self._my_app.get('/index')
        code, error=tidylib.tidy_document(response.body, options={'show-errors':1, 'show-warnings':0})
        self.assertFalse(error, '/index did not return valid html page')

    @unittest.expectedFailure
    def test_bookedit_unit(self):
        code, error=tidylib.tidy_document(self._my_class.bookedit(), options={'show-errors':1,'show-warnings':0})
        self.assertFalse(error, "method InventoryServer.bookedit does not return valid html page")
        
    def test_bookedit_functional(self):
        random_item=random.sample(list(Book.select()), 1)[0]
        response=self._my_app.get('/bookedit', {'id':random_item.id})
        code, error=tidylib.tidy_document(response.body, options={'show-errors':1, 'show-warnings':0})
        self.assertFalse(error, '/bookedit did not return valid html page')

    @unittest.expectedFailure
    def test_categoryedit_unit(self):
        code, error=tidylib.tidy_document(self._my_class.categoryedit(), options={'show-errors':1,'show-warnings':0})
        self.assertFalse(error, "method InventoryServer.categoryedit does not return valid html page")
        
    def test_categoryedit_functional(self):
        random_item=random.sample(list(Category.select()), 1)[0]
        response=self._my_app.get('/categoryedit', {'id':random_item.id})
        code, error=tidylib.tidy_document(response.body, options={'show-errors':1, 'show-warnings':0})
        self.assertFalse(error, '/categoryedit did not return valid html page')

    @unittest.expectedFailure
    def test_authoredit_unit(self):
        code, error=tidylib.tidy_document(self._my_class.authoredit(), options={'show-errors':1,'show-warnings':0})
        self.assertFalse(error, "method InventoryServer.authoredit does not return valid html page")
        
    def test_authoredit_functional(self):
        random_item=random.sample(list(Author.select()), 1)[0]
        response=self._my_app.get('/authoredit', {'id':random_item.id})
        code, error=tidylib.tidy_document(response.body, options={'show-errors':1, 'show-warnings':0})
        self.assertFalse(error, '/authoredit did not return valid html page')

    @unittest.expectedFailure
    def test_titleedit_unit(self):
        code, error=tidylib.tidy_document(self._my_class.titleedit(), options={'show-errors':1,'show-warnings':0})
        self.assertFalse(error, "method InventoryServer.titleedit does not return valid html page")
        
    def test_titleedit_functional(self):
        random_item=random.sample(list(Title.select()), 1)[0]
        response=self._my_app.get('/titleedit', {'id':random_item.id})
        code, error=tidylib.tidy_document(response.body, options={'show-errors':1, 'show-warnings':0})
        self.assertFalse(error, '/titleedit did not return valid html page')

    @unittest.expectedFailure
    def test_titlelist_unit(self):
        code, error=tidylib.tidy_document(self._my_class.titlelist(), options={'show-errors':1,'show-warnings':0})
        self.assertFalse(error, "method InventoryServer.titlelist does not return valid html page")
        
    def test_titlelist_functional(self):
        response=self._my_app.get('/titlelist')
        code, error=tidylib.tidy_document(response.body, options={'show-errors':1, 'show-warnings':0})
        self.assertFalse(error, '/titlelist did not return valid html page')

    @unittest.expectedFailure
    def test_search_unit(self):
        code, error=tidylib.tidy_document(self._my_class.search(), options={'show-errors':1,'show-warnings':0})
        self.assertFalse(error, "method InventoryServer.search does not return valid html page")
        
    def test_search_functional(self):
        response=self._my_app.get('/search')
        code, error=tidylib.tidy_document(response.body, options={'show-errors':1, 'show-warnings':0})
        self.assertFalse(error, '/search did not return valid html page')

    def test_search_returns_result(self):
        response=self._my_app.get('/search', {'title':'zinn'})
        self.assertTrue(response.body.count('Zinn'), '/search did not return results')
        
    @unittest.expectedFailure
    def test_titlelist_unit(self):
        code, error=tidylib.tidy_document(self._my_class.titlelist(), options={'show-errors':1,'show-warnings':0})
        self.assertFalse(error, "method InventoryServer.titlelist does not return valid html page")
        
    def test_titlelist_functional(self):
        response=self._my_app.get('/titlelist')
        code, error=tidylib.tidy_document(response.body, options={'show-errors':1, 'show-warnings':0})
        self.assertFalse(error, '/titlelist did not return valid html page')
    
def create_dynamic_method(reportItem):
    """just don't include `test` in the function name here, nose will try to
    run it"""
    def dynamic_test_method(self):
        """this function name doesn't matter much, it can start with `test`,
        but we're going to rename it dynamically below"""
        reportURLstring = '/report?reportname=' + reportItem.metadata['action']
        response=self._my_app.get(reportURLstring)
        code, error=tidylib.tidy_document(response.body, options={'show-errors':1, 'show-warnings':0})
        self.assertFalse(error, '%s did not return valid html page' % reportURLstring)
    return dynamic_test_method

for reportItem in InventoryServer().reportlist:
    dynamic_method = create_dynamic_method(reportItem)
    dynamic_method.__name__ = 'test_%s' % reportItem.metadata['name'].replace(' ', '_')
    setattr(Test_InventoryServer, dynamic_method.__name__, dynamic_method)





        
        
