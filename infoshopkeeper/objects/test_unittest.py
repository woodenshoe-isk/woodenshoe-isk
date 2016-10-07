import random
import unittest

from objects.book import Book
from objects.title import Title
from datetime import datetime

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
    
    
    
        
    
        
        
