import random
import unittest

from objects.book import Book
from objects.title import Title
from datetime import datetime

globals()['UNIT_TEST']=True

#class Book:
    #def object_to_form(self):
    #def _set_status(self, value):
class Test_Book(unittest.TestCase ):
    #def object_to_form
    #tested in object edit page
    
    #def _set_status
    def _set_status_STOCK(self):
        random_item=random.sample(list(Book.select(Book.q.status!='STOCK')), 1)[0]
        random_item_fields = list([string(x) for x in [radom_item.status, random_item.sold_when, random_item.inventoried_when]])
        random_item.status='STOCK'
        try:
            assertTrue(random_item.status=='STOCK')
            assertTrue(random_item.inventoried_when==random_item.sold_when)
        finally:
            random_item.status=random_item_fields[0]
            random_item.sold_when=random_item_fields[1]
        
    def _set_status_SOLD(self):
        random_item=random.sample(list(Book.select(Book.q.status!='SOLD')), 1)[0]
        random_item_fields = list([string(x) for x in [radom_item.status, random_item.sold_when, random_item.inventoried_when]])
        random_item.status='SOLD'
        try:
            assertTrue(random_item.status=='STOCK')
            assertTrue(random_item.inventoried_when==datetime.now().date())
        finally:
            random_item.status=random_item_fields[0]
            random_item.sold_when=random_item_fields[1]
        
#class Images(SQLObjectWithFormGlue):        
    #def retrieve_image(self, size='small'):
    #def retrieve_image_url(self, size='small'):
class Test_Images(unittest.TestCase ):
    def test_retrieve_image_url_have_image(self):
        pass
        random_item=random.sample(list(Title.select()), 1)[0]
        
    def test_retrieve_image_url_dont_have_image(self):
        pass
        
    def test_retrieve_image_url_malformed_remote_url(self):
        pass
    
    
    
        
    
        
        
'''class Test_Author
    class Test_sqlmeta:    def test__set_status
class Test_Category	class Test_sqlmeta:    class Test_sqlmeta:    def test__set_small_url
    def test__set_med_url
    def test__set_large_url
class Test_ISBN_to_be_entered
    class Test_sqlmeta
class Test_Kind
    class Test_sqlmeta
class Test_Location
    class Test_sqlmeta
class Test_Notes
    class Test_sqlmeta
class Test_SpecialOrder
    class Test_sqlmeta
    def test__get_contactInfo
    def test__set_contactInfo
    def test__get_customerName
    def test__set_customerName
class Test_SQLObjectWithFormGlue
    def test_form_to_object
    def test_object_to_form
    def test_handleForeignKey
    def test_handleEnum
    def test_handleString
    def test_handleUnicodeStr
    def test_handleFloat
    def test_handleBlob
    def test_handleDateTime
    def test_handleDate
    def test_class_to_form
    def test_handleForeignKey
    def test_handleEnum
    def test_handleString
    def test_handleUnicodeStr
    def test_handleFloat
        def test_handleBlob
        def test_handleDateTime
    def test_object_to_view
        def test_handleForeignKey
        def test_handleString
        def test_handleFloat
        def test_handleBlob
        def test_handleDateTime
    def test_safe
class Test_Title
    class Test_sqlmeta:
    def test_copies_in_status
    def test_authors_as_string
    def test_categories_as_string
    def test_distributors
    def test_distributors_as_string
    def test_last_book_inventoried
    def test_first_book_inventoried
    def test_highest_price_book
    def test_first_book_sold
    def test_last_book_sold
class Test_TitleSpecialOrder	
    class Test_sqlmeta:
class Test_Transaction
    class Test_sqlmeta:    
    def test_object_to_form
    def test_extracolumns
    def test_void
    def test_get_info'''
