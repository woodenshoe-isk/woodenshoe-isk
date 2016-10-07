import sys
import string
import sets
import datetime

from sqlobject import *
from tools import db
from objects.kind import Kind
from objects.images import Images
from SQLObjectWithFormGlue import SQLObjectWithFormGlue


class Title(SQLObjectWithFormGlue):
    class sqlmeta:
        fromDatabase = True

    booktitle=UnicodeCol(default=None)
    books = MultipleJoin('Book')
    author = RelatedJoin('Author', intermediateTable='author_title',createRelatedTable=True)
    specialorders = RelatedJoin('SpecialOrder', intermediateTable='title_special_order', createRelatedTable=False)
    specialorder_pivots = MultipleJoin('TitleSpecialOrder')
    images = SingleJoin('Images')
    categorys = MultipleJoin('Category')
    kind = ForeignKey('Kind')
    listTheseKeys=['kindID','kind']
    sortTheseKeys=[]
    
    
        
    def copies_in_status(self,status):
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
        return list(sets.Set([b.distributor for b in self.books]))

    def distributors_as_string(self):
        distributors=self.distributors()
        if distributors is not None:
            distributors=[d for d in distributors]
            return ', '.join(distributors)
        else:
            return ""
    
    def last_book_inventoried(self):
        try:
            last_book=None
            #get all books
            for b in self.books:
                #if there's not a book yet
                if not isinstance(objects.Book, last_book):
                   last_book=b 
                else:
                    #make last_book the newest book inventoried
                    if b.inventoried_when > last_book.inventoried_when:
                        last_book=b
        except:
            pass
        return last_book
        
    def first_book_inventoried(self):
        try:
            first_book=None
            #get all books
            for b in self.books:
                #if there's not a book yet
                if not isinstance(objects.Book, first_book):
                   first_book=b 
                else:
                    #make first_book the newest book inventoried
                    if b.inventoried_when < first_book.inventoried_when:
                        first_book=b
        except:
            pass
        if first_book:
           return first_book
        else:
           return None

    def highest_price_book(self):
        try:
            high_book=None
            #get all books
            for b in self.books:
                #if there's not a book yet
                if not isinstance(objects.Book, high_book):
                   high_book=b 
                else:
                    #make high_book the higest-priced book
                    if b.listprice > high_book.listprice:
                        high_book=b
        except:
            pass
        return high_book

    def first_book_sold(self):
        try:
            first_book=None
            #get all books
            for b in self.books:
                #if there's not a book yet that's 'SOLD'
                if b.status=="SOLD":
                    if not isinstance(objects.Book, first_book):
                       first_book=b 
                    else:
                        #make first_book oldest sold book
                        if b.sold_when < first_book.sold_when:
                            first_book=b
        except:
            pass
        return first_book
        
    def last_book_sold(self):
        try:
            last_book=None
            #get all books
            for b in self.books:
                #if there's not a book yet that's 'SOLD'
               if b.status=="SOLD":
                    if not isinstance(objects.Book, last_book):
                       last_book=b 
                    else:
                        #make last_book newest sold book
                        if b.sold_when > last_book.sold_when:
                            last_book=b
        except:
            pass
        return last_book
        
