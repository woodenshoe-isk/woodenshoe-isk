import sys
import string
import sets
import datetime

from etc import *

from sqlobject import *
from components import db
from SQLObjectWithFormGlue import SQLObjectWithFormGlue

 #Set up db connection
connection = connectionForURI('mysql://%s:%s@%s:3306/%s?debug=1&logger=MyLogger&loglevel=debug&use_unicode=1&charset=utf8'
% (dbuser,dbpass,dbhost,dbname))
sqlhub.processConnection = connection


#_connection = db.SQLObjconnect()

class dummybook:
    def __init__(self):
        self.sold_when="-"
        self.inventoried_when="-"
        self.dummy=True

class Title(SQLObjectWithFormGlue):
    class sqlmeta:
        fromDatabase = True
    #_connection = db.conn() 

    booktitle=UnicodeCol(default=None)
    books = MultipleJoin('Book')
    author = RelatedJoin('Author', intermediateTable='author_title',createRelatedTable=True)
    categorys = MultipleJoin('Category')
    kind = ForeignKey('Kind')
    listTheseKeys=['kindID','kind']
    sortTheseKeys=[]
    
    
    #~ _connection = db.conn()
    #~ books = MultipleJoin('Book')
    #~ author = RelatedJoin('Author', intermediateTable='author_title',createRelatedTable=True)
    #~ categorys = MultipleJoin('Category')
    #~ kind = ForeignKey('Kind')
    #~ listTheseKeys=('kind')

    #~ class sqlmeta:
        #~ fromDatabase = True
        
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
#    11/10/2008 - john fixed this manually
#       return string.join ([a.authorName for a in self.authors],",")
        try:
            return string.join ([a.authorName for a in self.author],",")
        except:
            return ""
    def categories_as_string(self):
        return string.join ([c.categoryName for c in self.categorys],",")

    def distributors(self):
        return list(sets.Set([b.distributor for b in self.books]))

    def distributors_as_string(self):
        distributors=self.distributors()
        if distributors is not None:
            distributors=[d for d in distributors if d is not None]
            return string.join(distributors,", ")
        else:
            return ""
    
    def last_book_inventoried(self):
        last_book=dummybook()
        try:
            for b in self.books:
                b.dummy=False
                if last_book.dummy==False:
                    if b.inventoried_when > last_book.inventoried_when:
                        last_book=b
                else:
                    last_book=b
        except:
            pass
        return last_book
    

    
    def first_book_inventoried(self):
        first_book=dummybook()
        try:
            for b in self.books:
                b.dummy=False
                if first_book.dummy==False:
                    if b.inventoried_when < first_book.inventoried_when:
                        first_book=b
                else:
                    first_book=b
        except:
            pass
        return first_book

    def highest_price_book(self):
        high_book=dummybook()
        try:
            for b in self.books:
                b.dummy=False
                
                if high_book.dummy==False:
                    if b.listprice > high_book.listprice:
                        high_book=b
                else:
                    high_book=b
        except:
            pass
        return high_book


        
    def last_book_sold(self):
        last_book=dummybook()
        try:
            for b in self.books:
                b.dummy=False
                if b.status=="SOLD":
                    if last_book.dummy==False:
                        if b.sold_when > last_book.sold_when:
                            last_book=b
                    else:
                        last_book=b
        except:
            pass
        return last_book

    def first_book_sold(self):
        first_book=dummybook()
        try:
            for b in self.books:
                b.dummy=False
                if b.status=="SOLD":
                    if first_book.dummy==False:
                        if b.sold_when < first_book.sold_when:
                            first_book=b
                    else:
                        first_book=b
        except:
            pass
        return first_book


