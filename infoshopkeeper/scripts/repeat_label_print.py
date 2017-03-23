import re
import gnureadline as readline
from sqlobject import sqlbuilder

from objects.book import Book
from objects.title import Title
from objects.location import Location

from printing import barcodeLabel

def rlinput(prompt, prefill=''):
    def hook(prefill):
        readline.insert_text(prefill)

    readline.set_startup_hook(hook)
    try:
        return raw_input(prompt)
    finally:
        readline.set_startup_hook()

should_quit = False
while should_quit != True:
    isbn  = raw_input('isbn or title >> ')
    if isbn.lower().strip() == 'quit' or isbn.lower().strip()=='q':
        should_quit=True
        continue
    if re.match('^[0-9]{13}$|^[0-9]{18}$', isbn):
        try:
            isbn, price = isbn[0:13], float(isbn[13, -1])
        except:
            isbn, price = isbn[0:13], 0.00
        titles = Title.selectBy(isbn=isbn)
        book = None
        if list(titles):
            for t1 in titles:
                ourprice = rlinput("price >> ", prefill=price)                                                             
                try:
                     float(ourprice)
                except:
                     continue
                books = Book.selectBy(titleID=t1.id, ourprice=float(ourprice), status='STOCK')
                if list(books):
                    ourprice = books[0].ourprice
                    listprice = books[0].listprice
                    book = books[0]
                    break
            if not book:        
                listprice = Book.selectBy(titleID=t1.id).max(Book.q.listprice) 
                book = Book(title=t1, status='STOCK', location=1, owner='woodenshoe', listprice=float(listprice), ourprice=float(ourprice), consignmentStatus='', distributor='', notes='')
            barcodeLabel.print_barcode_label(isbn=isbn, booktitle=t1.booktitle, ourprice=book.ourprice, listprice=listprice, num_copies=1)
        else:
            continue
    else:
        titles = Title.select(sqlbuilder.RLIKE(Title.q.booktitle, isbn))
        if list(titles):
            for n, t1 in enumerate(titles):
                print "%d. %s   %s" % (n, t1.booktitle, t1.type)
            n_book = int(raw_input("select book >> "))
            t1 = titles[n_book]
            price = raw_input('price >> ')
            listprice = Book.selectBy(titleID=t1.id).max(Book.q.listprice)
            book = Book(title=t1, status='STOCK', location=1, owner='woodenshoe', listprice=float(listprice), ourprice=float(price), consignmentStatus='', distributor='', notes='')
            barcodeLabel.print_barcode_label(isbn=t1.isbn, booktitle=t1.booktitle, ourprice=price, listprice=listprice, num_copies=1)
        else:   
             continue

