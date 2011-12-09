import mx.DateTime
import random
import unittest

from ecs import InvalidParameterValue

from objects.book import Book
from objects.title import Title

from tools.inventory import inventory
from tools import isbn

#class inventory:
    #def __init__(self):
    #def lookup_by_isbn(self,number):
    #def parseBrowseNodes(bNodes):
    #def parseBrowseNodesInner(item):
    #def addToInventory(self,title="",status="STOCK",authors=[],publisher="",listprice="",ourprice='',isbn="",categories=[],distributor="",location="",owner="",notes="",quantity=1,known_title=False,types='',kind_name="",extra_prices={}, tag=''):
    #def getInventory(self,queryTerms):
class test_inventory(unittest.TestCase):
    def test_lookup_by_isbn10_have_it(self):
        random_item= random.sample(list(Title.select('isbn RLIKE \'[0-9]{9}[0-9xX]\'')), 1)[0]
        result= inventory.lookup_by_isbn( random_item.isbn )
        self.assertEqual(random_item.isbn, result['isbn'], 'inventory.lookup_by_isbn returned wrong isbn for random isbn10 in database')
    def test_lookup_by_isbn10_dont_have(self):
        isbn_we_will_never_have='0060723467'      #Dick Cheney's autobiography
        result= inventory.lookup_by_isbn( isbn_we_will_never_have )
        self.assertEqual(isbn_we_will_never_have, result['isbn'] )
    def test_lookup_by_isbn10_is_invalid(self):
        #translation table of checkdigits to wrong ones (digit plus 1)
        tr_table=dict(zip( ['x', 'X'] + map(str, range(9, -1, -1)), ['0', '0', 'x'] + map(str, range(9, 0, -1)) ))
        random_item=random.sample(list(Title.select('isbn RLIKE \'[0-9]{9}[0-9xX]\'')), 1)[0]
        wrong_isbn=random_item.isbn[0:9] + tr_table[random_item.isbn[9]]
        self.assertRaises(InvalidParameterValue, inventory.lookup_by_isbn, wrong_isbn)
    def test_lookup_by_isbn13_is_valid(self):
        random_item=random.sample(list(Title.select('isbn RLIKE \'[0-9]{9}[0-9xX]\'')), 1)[0]
        converted_isbn=isbn.convert(random_item.isbn)
        result=inventory.lookup_by_isbn(converted_isbn)
        self.assertEqual(random_item.isbn, result['isbn'], 'inventory.lookup_by_isbn returned wrong isbn for random isbn in database')
    def test_lookup_by_isbn13_has_extra_spaces(self):
        random_item=random.sample(list(Title.select('isbn RLIKE \'[0-9]{9}[0-9xX]\'')), 1)[0]
        converted_isbn=isbn.convert(random_item.isbn)
        converted_isbn=converted_isbn[0:3]+' '+converted_isbn[3:8]+' '+converted_isbn[8:]
        result=inventory.lookup_by_isbn(converted_isbn)
        self.assertEqual(random_item.isbn, result['isbn'], 'inventory.lookup_by_isbn returned wrong isbn for random isbn in database')
    def test_lookup_by_isbn13_has_extra_hyphens(self):
        random_item=random.sample(list(Title.select('isbn RLIKE \'[0-9]{9}[0-9xX]\'')), 1)[0]
        converted_isbn=isbn.convert(random_item.isbn)
        converted_isbn=converted_isbn[0:3]+'-'+converted_isbn[3:8]+'-'+converted_isbn[8:]
        result=inventory.lookup_by_isbn(converted_isbn)
        self.assertEqual(random_item.isbn, result['isbn'], 'inventory.lookup_by_isbn returned wrong isbn for random isbn in database')
    def test_lookup_by_isbn13_is_invalid(self):
        random_item=random.sample(list(Title.select('isbn RLIKE \'[0-9]{9}[0-9xX]\'')), 1)[0]
        converted_isbn=isbn.convert(random_item.isbn)
        wrong_isbn=converted_isbn[0:12] + str((int(converted_isbn[12]) + 1) % 10)
        result=inventory.lookup_by_isbn(wrong_isbn)
        self.assertEqual(random_item.isbn, result['isbn'], 'inventory.lookup_by_isbn returned wrong isbn for invalid isbn13')
    def test_lookup_by_isbn_is_reg(self):
        random_item=random.sample(list(Title.select('isbn RLIKE \'reg [0-9]{3,5}\'')), 1)[0]
        result=inventory.lookup_by_isbn(random_item.isbn)
        self.assertEqual(random_item.isbn, result['isbn'], 'inventory.lookup_by_isbn returned wrong isbn for random isbn (reg) in database')
    def test_lookup_by_isbn_is_wsr(self):
        random_item=random.sample(list(Title.select('isbn RLIKE \'wsr [0-9]{3,5}\'')), 1)[0]
        result=inventory.lookup_by_isbn(random_item.isbn)
        self.assertEqual(random_item.isbn, result['isbn'], 'inventory.lookup_by_isbn returned wrong isbn for random isbn (wsr) in database')
    def test_addToInventory_have_title(self):
        random_item=random.sample(list(Book.selectBy(status='STOCK')), 1)[0]
        fakeargs=dict(title=random_item.title.booktitle, authors=random_item.title.authors_as_string(), publisher=random_item.title.publisher, distributor=random_item.distributor, owner='woodenshoe', listprice=random_item.listprice, ourprice=random_item.ourprice, isbn=random_item.title.isbn, categories=random_item.title.categories_as_string(), location=random_item.location.locationName, quantity=1, known_title=True, types=random_item.title.type, kind_name=random_item.title.kind.kindName)
        inventory.addToInventory( **fakeargs )
        today=mx.DateTime.now().strftime('%Y-%m-%d')
        confirm=Book.selectBy(titleID=random_item.titleID).filter('inventoried_when=%s' % today)
        try:
            self.assertTrue(confirm, "inventory.addToInventory of title that we have does not add item to inventory")
        finally:
            print "confirm: ", list(confirm), confirm[-1]
            confirm[-1].destroySelf()
    def test_addToInventory_dont_have_title(self):
        pass
#     def test_getInventory_title(self):
#         random_item=random.sample(list(Book.selectBy(status='STOCK')), 1)[0]
#         result=inventory.getInventory(title=random_item.title.booktitle).count()
#         assertTrue(result, 'inventory.getInventory does not get books by title') 
#     def test_getInventory_status_stock(self):
#         random_item=random.sample(list(Book.selectBy(status='STOCK')), 1)[0]
#         result=inventory.getInventory(status='STOCK').count()
#         assertTrue(result, 'inventory.getInventory does not get books by status \'STOCK\'') 
#     def test_getInventory_author(self):
#         random_item=random.sample(list(Book.selectBy(status='STOCK')), 1)[0]
#         result=inventory.getInventory(author=random_item.title.author[0].authorName).count()
#         assertTrue(result, 'inventory.getInventory does not get books by author') 
#     def test_getInventory_publisher(self):
#         random_item=random.sample(list(Book.selectBy(status='STOCK')), 1)[0]
#         result=inventory.getInventory(publisher=random_item.title.publisher).count()
#         assertTrue(result, 'inventory.getInventory does not get books by publisher') 
#     def test_getInventory_isbn(self):
#         random_item=random.sample(list(Book.selectBy(status='STOCK')), 1)[0]
#         result=inventory.getInventory(publisher=random_item.title.isbn).count()
#         assertTrue(result, 'inventory.getInventory does not get books by isbn') 
#     def test_getInventory_category(self):
#         random_item=random.sample(list(Book.selectBy(status='STOCK')), 1)[0]
#         result=inventory.getInventory(category=random_item.title.categorys[0]).count()
#         assertTrue(result, 'inventory.getInventory does not get books by category') 
#     def test_getInventory_distributor(self):
#         random_item=random.sample(list(Book.selectBy(status='STOCK')), 1)[0]
#         result=inventory.getInventory(distributor=random_item.distributor).count()
#         assertTrue(result, 'inventory.getInventory does not get books by distributor') 
#     def test_getInventory_location(self):
#         random_item=random.sample(list(Book.selectBy(status='STOCK')), 1)[0]
#         result=inventory.getInventory(location=random_item.location).count()
#         assertTrue(result, 'inventory.getInventory does not get books by location') 
#     def test_getInventory_owner(self):
#         random_item=random.sample(list(Book.selectBy(status='STOCK')), 1)[0]
#         result=inventory.getInventory(owner=random_item.owner).count()
#         assertTrue(result, 'inventory.getInventory does not get books by owner') 
#     def test_getInventory_quantity(self):
#         pass
#     def test_getInventory_types(self):
#         pass
#     def test_getInventory_kind(self):
#         pass
#     def test_getInventory_tag(self):
#         pass
#     
    
    