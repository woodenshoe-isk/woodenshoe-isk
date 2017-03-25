from time import time, asctime, localtime, sleep
import types, string

from . import ecs
from config.config import configuration 


from objects.title import Title
from objects.book import Book
from objects.author import Author
from objects.category import Category
from objects.images import Images
from objects.kind import Kind
from objects.location import Location
from objects.title import Title
from objects.title_special_order import TitleSpecialOrder

import isbnlib

import sys
import re

from sqlobject.sqlbuilder import Field, RLIKE, AND, LEFTJOINOn
from MySQLdb import escape_string

amazon_license_key=configuration.get('amazon_license_key')
amazon_secret_key=configuration.get('amazon_secret_key')
amazon_associate_tag=configuration.get('amazon_associate_tag')
default_kind=configuration.get('default_kind')

def process_isbn(isbn):
    print("in process_isbn. isbn is ", isbn, file=sys.stderr)
    #only strip quotes if wsr, reg, or consignment number, or none
    if re.match('^wsr|^reg|^\d{2,4}-\d{1,4}$|n/a|none', isbn, re.I):
        isbn = re.sub('[\'\"]', '', isbn)
        price = None
    #strip quotes, dashes and whitespace. convert isbn10 to isbn13.
    #split isbn and price if it's an extended isbn
    else:
        isbn=re.sub('[\s\'\"\-]', '', isbn)
        price = None
        #note the checking for the first character of ean5 extension
        #if it's 5, it means price is in us dollars 0-99.99
        #otherwise, we need to do price ourself.
        if len(isbn)==18:
            if isbn[-5] == '5':
                price = float(isbn[-4:])/100
            isbn=isbn[:-5]
        if len(isbn)==10:
            if isbnlib.is_isbn10(isbn):
                isbn=isbnlib.to_isbn13(isbn)
            else:
                #Fix this -- shouldn't be here.
                #investigate why amazon gives InvalidParameterCombination ins
                raise ecs.InvalidParameterValue
    return isbn, price

def lookup_by_isbn(number, forceUpdate=False):
    isbn, price = process_isbn(number)
    print(isbn, price, file=sys.stderr)
    if (len(isbn)>0 and not re.match('^n(\s|/){0,1}a|none', isbn, re.I)):
        #first we check our database
        titles =  Title.select(Title.q.isbn==isbn)
        ##print titles #debug
        known_title= False
        the_titles=list(titles)
        if (len(the_titles) > 0) and ( not forceUpdate ):
            ##print "in titles"
            known_title= the_titles[0]
            ProductName = the_titles[0].booktitle.format()
            authors=[]
            if len(the_titles[0].author) > 0:
                authors = [x.authorName.format() for x in the_titles[0].author]
            authors_as_string = ', '.join(authors)
            categories=[]
            if len(the_titles[0].categorys) > 0:
                ##print len(the_titles[0].categorys)
                ##print the_titles[0].categorys
                categories = [x.categoryName.format() for x in the_titles[0].categorys] 
            categories_as_string = ', '.join(categories)
            if len(the_titles[0].books) > 0:
                ListPrice = max([x.listprice for x in the_titles[0].books])
            else:
                ListPrice = 0
            Manufacturer = the_titles[0].publisher.format()
            Format=the_titles[0].type.format()
            Kind=the_titles[0].kind.kindName
            orig_isbn=the_titles[0].origIsbn.format()
            if the_titles[0].images:
                 large_url = the_titles[0].images.largeUrl
                 med_url = the_titles[0].images.medUrl
                 small_url = the_titles[0].images.smallUrl
            else:
                 large_url = med_url = small_url = ''

            SpecialOrders=[tso.id for tso in Title.selectBy(isbn=isbn).throughTo.specialorder_pivots.filter(TitleSpecialOrder.q.orderStatus=='ON ORDER')]
            return {"title":ProductName,
                "authors":authors,
                "authors_as_string":authors_as_string,
                "categories_as_string":categories_as_string,
                "list_price":ListPrice,
                "publisher":Manufacturer,
                "isbn":isbn,
                "orig_isbn":orig_isbn,
                "large_url":large_url,
                "med_url":med_url,
                "small_url":small_url,
                "format":Format,
                "kind":Kind,
                "known_title": known_title,
                "special_order_pivots":SpecialOrders}
        else: #we don't have it yet
            ##print "in isbn"
            sleep(1) # so amazon doesn't get huffy 
            ecs.setLicenseKey(amazon_license_key)
            ecs.setSecretAccessKey(amazon_secret_key)
            ecs.setAssociateTag(amazon_associate_tag)
             
            ##print "about to search", isbn, isbn[0]
            amazonBooks=[]
             
            idType=''
            if len(isbn)==12:
                idType='UPC'
            elif len(isbn)==13:
                #if we are using an internal isbn
                if isbn.startswith('199'):
                    return []
                #otherwise search on amazon.
                elif isbn.startswith('978') or isbn.startswith('979'):
                    idType='ISBN'
                else:
                    idType='EAN'
            
            print("idtype ",  idType, file=sys.stderr)
            try:
                    print( isbn, idType, file=sys.stderr)
                    amazonBooks = ecs.ItemLookup(isbn,IdType= idType, SearchIndex="Books",ResponseGroup="ItemAttributes,BrowseNodes,Images")
            except ecs.InvalidParameterValue:
                pass
            ##print pythonBooks
            if amazonBooks:
                result={}
                authors=[]
                categories=[]
                
                len_largest = 0
                for book in amazonBooks:
                    if len_largest < len(dir(book)):
                        len_largest = len(dir(book))
                        book_for_info = book 

                for x in ['Author', 'Creator', 'Artist', 'Director']:
                    if hasattr(book_for_info, x):
                        if isinstance(getattr(book_for_info, x), type([])):
                            authors.extend(getattr(book_for_info, x))
                        else:
                            authors.append(getattr(book_for_info, x))
             

                authors_as_string = ', '.join(authors)

                categories_as_string =""
             
                # a bit more complicated of a tree walk than it needs be.
                # set up to still have the option of category strings like "history -- us"
                # switched to sets to quickly remove redundancies.
                def parseBrowseNodes(bNodes):
                    def parseBrowseNodesInner(item):
                        bn=set()
                        if hasattr(item, 'Name'):
                            bn.add(item.Name)
                        if hasattr(item, 'Ancestors'):
                            ##print "hasansc"   
                            for i in item.Ancestors:
                                bn.update(parseBrowseNodesInner(i))
                        if hasattr(item, 'Children'):
                            for i in item.Children:
                                bn.update(parseBrowseNodesInner(i))
                                ##print "bn ", bn
                        if not (hasattr(item, 'Ancestors') or hasattr(item, 'Children')):            
                            if hasattr(item, 'Name'):
                                return set([item.Name])
                            else:
                                return set()
                        return bn
                    nodeslist=[parseBrowseNodesInner(i) for i in bNodes ]
                    nodes=set()
                    for n in nodeslist:
                        nodes = nodes.union(n)
                    return nodes


                categories=parseBrowseNodes(book_for_info.BrowseNodes)
                categories_as_string = ', '.join(categories)


                ProductName=""
                if hasattr(book_for_info, 'Title'):
                    ProductName=book_for_info.Title

                 
                Manufacturer=""
                if hasattr(book_for_info, 'Manufacturer'):
                    Manufacturer=book_for_info.Manufacturer

                ListPrice=""
                if hasattr(book_for_info, 'ListPrice'):
                    ListPrice=book_for_info.ListPrice.FormattedPrice.replace("$", '')

                Format=''
                if hasattr(book_for_info, "Binding"):
                    Format=book_for_info.Binding
             
                Kind=''
                if book_for_info.ProductGroup=='Book':
                    Kind='books'
                elif book_for_info.ProductGroup=='Music':
                    Kind='music'
                elif book_for_info.ProductGroup in ('DVD', 'Video'):
                    Kind='film'
                
                if hasattr(book_for_info, "LargeImage"):
                    large_url=book_for_info.LargeImage.URL
                else:
                    large_url=''

                if hasattr(book_for_info, "MediumImage"):
                    med_url=book_for_info.MediumImage.URL
                else:
                    med_url=''

                if hasattr(book_for_info, "SmallImage"):
                    small_url=book_for_info.SmallImage.URL
                else:
                    small_url=''
             
                return {"title":ProductName,
                    "authors":authors,
                    "authors_as_string":authors_as_string,
                    "categories_as_string":categories_as_string,
                    "list_price":ListPrice,
                    "publisher":Manufacturer,
                    "isbn":isbn,
                    "orig_isbn":isbn,
                    "large_url":large_url,
                    "med_url":med_url,
                    "small_url":small_url,
                    "format":Format,
                    "kind":Kind,
                    "known_title": known_title,
                    "special_orders": []}
            else:
                isbnlibbooks=[]
                isbnlibbooks = isbnlib.meta('isbn')
                
                if isbnlibbooks:
                    return {"title":isbnlibBooks.Title,
                        "authors":isbnlibBooks.Authors,
                        "authors_as_string":','.join(isbnlibBooks.Authors),
                        "categories_as_string":None,
                        "list_price":0.00,
                        "publisher":isbnlibBooks.Publisher,
                        "isbn":isbn,
                        "orig_isbn":isbn,
                        "large_url":None,
                        "med_url":None,
                        "small_url":None,
                        "format":None,
                        "kind":'book',
                        "known_title": known_title,
                        "special_orders": []}  
                else:
                    return []
         
    
    else:
        return []
     
def search_by_keyword(authorOrTitle=''):
    def database_gen(authorOrTitle=''):
        titles=[]
         
        #start out with the join clauses in the where clause list
        where_clause_list = []
        clause_tables=['book', 'author', 'author_title',]
        join_list=[LEFTJOINOn('title', 'book', 'book.title_id=title.id'), LEFTJOINOn(None, 'author_title', 'title.id=author_title.title_id'), LEFTJOINOn(None, 'author', 'author.id=author_title.author_id')]
         
        #add filter clauses if they are called for
        where_clause_list.append("(author.author_name RLIKE '%s' OR title.booktitle RLIKE '%s')" % (authorOrTitle.strip(), authorOrTitle.strip()))
        #AND all where clauses together
        where_clause=' AND '.join(where_clause_list)
        titles=[]
         
        #do search. 
        titles=Title.select( where_clause, join=join_list, clauseTables=clause_tables, distinct=True)
        for t1 in titles:
            yield { "title":t1.booktitle,
                    'authors':t1.author,
                    'authors_as_string':t1.authors_as_string(),
                    'categories_as_string':t1.categories_as_string(),
                    'list_price':t1.highest_price_book().ourprice,
                    'publisher':t1.publisher,
                    'isbn':t1.isbn,
                    'format': t1.type, 
                    'kind':t1.kind.kindName,
                    'known_title':t1}
                     
    def amazon_gen(authorOrTitle=''):
        sleep(1) # so amazon doesn't get huffy 
        ecs.setLicenseKey(amazon_license_key)
        ecs.setSecretAccessKey(amazon_secret_key)
        ecs.setAssociateTag(amazon_associate_tag)
         
        iter1 = ecs.ItemSearch(Keywords='python', SearchIndex='Books', ResponseGroup="ItemAttributes,BrowseNodes")
        #iter1=xrange(0,20)
        def process_data(data):
            result={}
            authors=[]
            categories=[]
     
            for x in ['Author', 'Creator', 'Artist', 'Director']:
                if hasattr(data, x):
                    if isinstance(getattr(data, x), type([])):
                        authors.extend(getattr(data, x))
                    else:
                        authors.append(getattr(data, x))
             
     
            authors_as_string = ', '.join(authors)
     
            categories_as_string =""
             
            # a bit more complicated of a tree walk than it needs be.
            # set up to still have the option of category strings like "history -- us"
            # switched to sets to quickly remove redundancies.
            def parseBrowseNodes(bNodes):
                def parseBrowseNodesInner(item):
                    bn=set()
                    if hasattr(item, 'Name'):
                        bn.add(item.Name)
                    if hasattr(item, 'Ancestors'):
                        ##print "hasansc"   
                        for i in item.Ancestors:
                            bn.update(parseBrowseNodesInner(i))
                    if hasattr(item, 'Children'):
                        for i in item.Children:
                            bn.update(parseBrowseNodesInner(i))
                            ##print "bn ", bn
                    if not (hasattr(item, 'Ancestors') or hasattr(item, 'Children')):            
                        if hasattr(item, 'Name'):
                            return set([item.Name])
                        else:
                            return set()
                    return bn
                nodeslist=[parseBrowseNodesInner(i) for i in bNodes ]
                nodes=set()
                for n in nodeslist:
                    nodes = nodes.union(n)
                return nodes
     
     
            categories=parseBrowseNodes(data.BrowseNodes)
            categories_as_string = ', '.join(categories)
     
     
            ProductName=""
            if hasattr(data, 'Title'):
                ProductName=data.Title
     
                 
            Manufacturer=""
            if hasattr(data, 'Manufacturer'):
                Manufacturer=data.Manufacturer
     
            ListPrice=""
            if hasattr(data, 'ListPrice'):
                ListPrice=data.ListPrice.FormattedPrice.replace("$", '')
     
            Format=''
            if hasattr(data, "Binding"):
                Format=data.Binding
             
            ISBN=''
            if hasattr(data, "ISBN"):
                ISBN=data.ISBN
            elif hasattr(data, "EAN"):
                ISBN=data.EAN
                 
            Kind=''
            if data.ProductGroup=='Books':
                Kind='books'
            elif data.ProductGroup=='Music':
                Kind='music'
            elif data.ProductGroup in ('DVD', 'Video'):
                Kind='film'
             
            return {"title": ProductName,
                "authors": authors,
                "authors_as_string": authors_as_string,
                "categories_as_string": categories_as_string,
                "list_price": ListPrice,
                "publisher": Manufacturer,
                "isbn": ISBN,
                "format": Format,
                "kind": Kind,
                "known_title": None,}
     
        return (process_data(a) for a in ecs.ItemSearch(Keywords=authorOrTitle, SearchIndex='Books', ResponseGroup="ItemAttributes,BrowseNodes"))
     
    print('at ', authorOrTitle, file=sys.stderr)
    iter_array = [database_gen]
    #test if internet is up
    try:
        urllib.request.urlopen('http://google.com', timeout=1)
    except:
        pass
    else:
        iter_array.append(amazon_gen)
     
    print("iterarray ", iter_array, file=sys.stderr)
    for iter1 in iter_array:
        try:
            iter1=iter1(authorOrTitle)
        except IOError as err:
            print(err)
            yield
        except Exception as err:
            print(err)
            yield
        else:
            print(iter1)
            for element in iter1:
                try:
                    yield element
                except IOError as err:
                    print(err)
                    yield
                 
def addToInventory(title="",status="STOCK",authors=None,publisher="",listprice="",ourprice='',isbn="", orig_isbn='',categories=[],distributor="",location='', location_id='',large_url='',med_url='',small_url='',owner="",notes="",quantity=1,known_title=False,types='',kind_name="",kind=default_kind, extra_prices={}, tag='', num_copies=0, printlabel=False, special_orders=0):
    print("GOT to addToInventory", file=sys.stderr)
    if not authors:
        authors = []
    if known_title:
        print("known_title ", known_title, file=sys.stderr)
        if not known_title.booktitle:
            known_title.booktitle = title
        if not known_title.publisher:
            known_title.publisher = publisher
        if not known_title.type:
            known_title.type = types
    elif not(known_title):
        print("unknown title", file=sys.stderr)
        #add a title
        the_kinds=list(Kind.select(Kind.q.kindName==kind))
        kind_id = None
        if the_kinds:
            kind_id = the_kinds[0].id
        print('kind id is', kind_id, file=sys.stderr)

        #print>>sys.stderr, title
         
        title=title.encode('utf8', "backslashreplace")
        publisher=publisher
        #print>>sys.stderr, title, publisher
        known_title=Title(isbn=isbn, origIsbn=orig_isbn, booktitle=title, publisher=publisher, tag=" ", type=types, kindID=kind_id)
        print(known_title, file=sys.stderr)
        
        im=Images(titleID=known_title.id, largeUrl=large_url, medUrl=med_url, smallUrl=small_url)
        print(im, file=sys.stderr)
        
        for rawAuthor in authors:
            author = rawAuthor.encode("utf8", "backslashreplace")
            theAuthors = Author.selectBy(authorName=author)
            theAuthorsList = list(theAuthors)
            if len(theAuthorsList) == 1:
                known_title.addAuthor(theAuthorsList[0])
            elif len(theAuthorsList) == 0:
                a = Author(authorName=author)
                known_title.addAuthor(a)
            else:
                # We should SQLDataCoherenceLost here
                print("mmm... looks like you have multiple author of the sama name in your database...", file=sys.stderr)
        for category in categories:
            Category(categoryName=category.encode("utf8", "backslashreplace"), title=known_title)
    #the_locations=list(Location.select(Location.q.locationName==location))
    #location_id=1
    #if the_locations:
    #    location_id = the_locations[0].id
    if not ourprice:
        ourprice=listprice
    print("about to enter book loop", file=sys.stderr)
    print("location is", location, file=sys.stderr)
    print("location_id is", location_id, file=sys.stderr)
    for i in range(int(quantity)): 
        print("book loop", file=sys.stderr)
        b=Book(title=known_title, status=status, distributor=distributor.encode('ascii', "backslashreplace"), listprice=listprice, ourprice=ourprice, location=int(location_id), owner=owner.encode("utf8", "backslashreplace"), notes=notes.encode("utf8", "backslashreplace"), consignmentStatus="")
#               book_for_info.extracolumns()
#~ #               for mp in extra_prices.keys():
#                   setattr(book_for_info,string.replace(mp," ",""),extra_prices[mp])


def searchInventory(sortby='booktitle', out_of_stock=False, **kwargs):
    #start building the filter list
    where_clause_list = []
    print("kwargs are ", kwargs, file=sys.stderr)
    for k in kwargs:
        if type(k)==bytes:
            kwargs[k] = kwargs[k].decode('utf-8')
    to_delete = [k for k in kwargs if kwargs[k] == '']
    for td in to_delete:
        del kwargs[td]
    print(len(kwargs), file=sys.stderr)
    clause_tables=['book', 'author', 'author_title', 'category', 'location']
    join_list=[LEFTJOINOn('title', 'book', 'book.title_id=title.id'), LEFTJOINOn(None, 'author_title', 'title.id=author_title.title_id'), LEFTJOINOn(None, 'author', 'author.id=author_title.author_id'), LEFTJOINOn(None, Category, Category.q.titleID==Title.q.id), LEFTJOINOn(None, Location, Location.q.id==Book.q.locationID)]
    if 'the_kind' in kwargs:
        where_clause_list .append("title.kind_id = '%s'" % kwargs['the_kind'])
    if 'the_location' in kwargs and len(the_location)>1:
        where_clause_list .append("book.location_id = '%s'" % kwargs['the_location'])
    if 'title' in kwargs:
        where_clause_list.append("title.booktitle RLIKE '%s'" % kwargs['title'].strip())
    if 'publisher' in kwargs:
        where_clause_list.append("title.publisher RLIKE '%s'" % kwargs['publisher'].strip())
    if 'tag' in kwargs:
        where_clause_list.append("title.tag RLIKE '%s'" % kwargs['tag'].strip())
    if 'isbn' in kwargs:
        isbn, price=process_isbn(kwargs['isbn'])
        where_clause_list.append("title.isbn RLIKE '%s'" % kwargs['isbn'])
    if 'formatType' in kwargs:
        where_clause_list.append("title.type RLIKE '%s'" % kwargs['formatType'].strip())
    if 'owner' in kwargs:
        where_clause_list.append("book.owner RLIKE '%s'" % kwargs['owner'].strip())
    if 'distributor' in kwargs:
        where_clause_list.append("book.distributor RLIKE '%s'" % kwargs['distributor'].strip())
    if 'inv_begin_date' in kwargs:
        where_clause_list.append("book.inventoried_when >= '%s'" % kwargs['inv_begin_date'])
    if 'inv_end_date' in kwargs:
        where_clause_list.append("book.inventoried_when < '%s'" % kwargs['inv_end_date'])
    if 'sold_begin_date' in kwargs:
        where_clause_list.append("book.sold_when >= '%s'" % kwargs['sold_begin_date'])
    if 'sold_end_date' in kwargs:
        where_clause_list.append("book.sold_when < '%s'" % kwargs['sold_end_date'])
    if 'author' in kwargs:
        where_clause_list.append("author.author_name RLIKE '%s'" % kwargs['author'].strip())
    if 'category' in kwargs:
        where_clause_list.append("category.category_name RLIKE '%s'" % kwargs['category'].strip())
    if 'status' in kwargs:
        where_clause_list.append("book.status = '%s'" % kwargs['status'].strip())
    if 'id' in kwargs:
        where_clause_list.append("title.id=%s" % kwargs['id'])
    if 'authorOrTitle' in kwargs:
        where_clause_list.append("(author.author_name RLIKE '%s' OR title.booktitle RLIKE '%s')" % (kwargs['authorOrTitle'].strip(), kwargs['authorOrTitle'].strip()))

    where_clause=' AND '.join(where_clause_list)
     
    #do search first. Note it currently doesnt let you search for every book in database, unless you use some sort of
    #trick like '1=1' for the where clause string, as the where clause string may not be blank
    titles=[]
    if len(kwargs)>1 or kwargs.setdefault('out_of_stock', False):
        titles=Title.select( where_clause, join=join_list, orderBy=sortby, clauseTables=clause_tables, distinct=True)
    #filter for stock status
    if 'out_of_stock' in kwargs:
        titles = [t for t in titles if t.copies_in_status("STOCK") == 0]
    #filter on specific numbers in stock
    if 'stock_less_than' in kwargs:
        titles = [t for t in titles if t.copies_in_status("STOCK") <= int(kwargs['stock_less_than'])]
    if 'stock_more_than' in kwargs:
        titles = [t for t in titles if t.copies_in_status("STOCK") >= int(kwargs['stock_more_than'])]
    #filter by items sold
    if 'sold_more_than' in kwargs:
        titles = [t for t in titles if t.copies_in_status("SOLD") >= int(kwargs['sold_more_than'])]
    if 'sold_less_than' in kwargs:
        titles = [t for t in titles if t.copies_in_status("SOLD") >= int(kwargs['sold_less_than'])]
    print(titles, file=sys.stderr)
    return titles

def getInventory(queryTerms):
    print( queryTerms, file=sys.stderr)
    keys=list(queryTerms)
    print("keys are ", keys)
    for k in keys:
        if type(queryTerms[k])==bytes:
            queryTerms[k] = queryTerms[k].decode('utf-8')
     
    isbnSelect=""
    kindSelect=""
    statusSelect=""
    titleSelect=""
    authorSelect=""
    categorySelect=""
    clauseTables=[]

    if "kind" in keys: # joins suck, avoid if possible
        kind_map={}
        for k in [(x.kindName, x.id) for x in list(Kind.select())]:
            kind_map[k[0]]=k[1]
        try:
            kind_id=kind_map[queryTerms['kind']]
            kindSelect=Book.sqlrepr(AND(Field("book", "title_id")==Field("title", "id"), Field("title", "kind_id")==kind_id))
        except: 
            pass
         
    if 'status' in keys:
        statusSelect=Book.sqlrepr(Field("book", "status")==queryTerms["status"])
         

    if ('title' in keys) or ('authorName' in keys) or ('kind' in keys) or ('categoryName' in keys) or ('isbn' in keys):
        clauseTables.append('title') 
        #we are going to need to do a join 

        if 'title' in keys:
            titleSelect=Book.sqlrepr(AND(Field("book", "title_id")==Field("title", "id"), RLIKE(Field("title", "booktitle"), queryTerms["title"])))


        if 'isbn' in keys:
            isbn, price = process_isbn(queryTerms['isbn'])
            print("isbn and price are ", isbn, price)
            titleSelect=Book.sqlrepr(AND(Field("book", "title_id")==Field("title", "id"), Field("title", "isbn")==isbn))


        if 'authorName' in keys:
            #authorSelect="""book.title_id = title.id AND author.title_id=title.id AND author.author_name RLIKE %s""" % (Book.sqlrepr(queryTerms["authorName"]))    
           authorSelect=Book.sqlrepr(AND(Field("book", "title_id")==Field("title", "id"), Field("author", "id")==Field("author_title", "author_id"), Field("title", "id")==Field("author_title", "title_id"), RLIKE(Field("author", "author_name"), queryTerms["authorName"])))
           clauseTables.append('author')
           clauseTables.append('author_title')
         
        if 'categoryName' in keys:
            categorySelect="""book.title_id = title.id AND category.title_id=title.id AND category.category_name RLIKE %s""" % (Book.sqlrepr(queryTerms["categoryName"]))
            clauseTables.append('category')
    try:
        books=Book.select(
            " AND ".join([term for term in [statusSelect, titleSelect, authorSelect, kindSelect, categorySelect] if term !=""]),
            clauseTables=clauseTables,
            distinct=True    )
    except TypeError:
        books=Book.select(
            " AND ".join([term for term in [statusSelect, titleSelect, authorSelect, kindSelect, categorySelect] if term !=""]),
            clauseTables=clauseTables   )

    results={}
    i=1
    for book_for_info in books:
        theTitle=book_for_info.title.booktitle
        authorString = ", ".join([a.authorName for a in book_for_info.title.author])
        categoryString = ", ".join([c.categoryName for c in book_for_info.title.categorys])
        results[i]=(theTitle.capitalize(),
                    authorString, 
                    book_for_info.listprice  if book_for_info.listprice is not None else '',
                    book_for_info.title.publisher if book_for_info.title.publisher is not None else '',
                    book_for_info.status if book_for_info.status is not None else'',
                    book_for_info.title.isbn,
                    book_for_info.distributor if book_for_info.distributor is not None else '',
                    book_for_info.location.locationName if book_for_info.location is not None else '',
                    book_for_info.notes if book_for_info.notes is not None else '',
                    book_for_info.id,
                    book_for_info.title.kind and book_for_info.title.kind.kindName if book_for_info.title.kind is not None else '',
        categoryString,
        book_for_info.title.type if book_for_info.title.type is not None else '')
    return results
    
def updateItem(id):
    title = Title.get(id)
    title_info = lookup_by_isbn( title.orig_isbn, forceUpdate=True)
        
        

