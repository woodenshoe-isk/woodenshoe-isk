import sys
import string
#import sets
import datetime

from sqlobject import *
from tools import db
from objects.kind import Kind
from objects.images import Images
from .SQLObjectWithFormGlue import SQLObjectWithFormGlue


class Title(SQLObjectWithFormGlue):
    class sqlmeta:
        fromDatabase = True

    booktitle=UnicodeCol(default=None)
    books = MultipleJoin('Book')
    author = RelatedJoin('Author', intermediateTable='author_title', createRelatedTable=True)
    specialorders = RelatedJoin('SpecialOrder', intermediateTable='title_special_order', createRelatedTable=False)
    specialorder_pivots = MultipleJoin('TitleSpecialOrder')
    images = SingleJoin('Images')
    categorys = MultipleJoin('Category')
    kind = ForeignKey('Kind')
    listTheseKeys=['kindID', 'kind']
    sortTheseKeys=[]
    
    
        
    def copies_in_status(self, status):
        i=0
        try:
            for b in self.books:
                if b.status==status:
                    i=i+1
        except:
            pass

        return i

    def authors_as_string(self):
        try:
            return ', '.join ([a.authorName for a in self.author])
        except:
            return ""

    def categories_as_string(self):
        try:
            return ', '.join ([c.categoryName for c in self.categorys])
        except:
            return ''
            
    def distributors(self):
        return list(set([b.distributor for b in self.books]))

    def distributors_as_string(self):
        distributors=self.distributors()
        if distributors is not None:
            distributors=[d for d in distributors]
            return ', '.join(distributors)
        else:
            return ""
    
    def last_book_inventoried(self):
        try:
            return sorted(self.books, key=lambda x:  x.inventoried_when, reverse=True)[0]
        except:
            return ''

    
    def first_book_inventoried(self):
        try:
            return sorted(self.books, key=lambda x:  x.inventoried_when, reverse=False)[0]
        except:
            return ''


    def highest_price_book(self):
         try:
            return sorted(self.books, key=lambda x:  x.ourprice, reverse=True)[0]
         except:
            return ''
                                       
    def first_book_sold(self):
        try:
            return sorted([x for x in self.books if x.status=='SOLD'], key=lambda x:  x.sold_when, reverse=False)[0]
        except:
            return ''

    def last_book_sold(self):
        try:
            return sorted([x for x in self.books if x.status=='SOLD'], key=lambda x:  x.sold_when, reverse=True)[0]
        except:
            return ''
