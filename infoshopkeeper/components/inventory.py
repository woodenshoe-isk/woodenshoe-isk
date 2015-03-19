from time import time,asctime,localtime,sleep
import types,string
 
import ecs
from etc import amazon_license_key,amazon_secret_key, amazon_associate_tag, default_kind
from objects.title import Title
from objects.book import Book
from objects.author import Author
from objects.category import Category
from objects.kind import Kind
from objects.location import Location
from objects.title import Title
from objects.title_special_order import TitleSpecialOrder

import tools.isbn as isbnlib
from upc import upc2isbn

import sys
import re
 
from sqlobject.sqlbuilder import Field, RLIKE, AND, LEFTJOINOn
from MySQLdb import escape_string
 
class inventory(object):
    def __init__(self):
        x=1
     
        
    @staticmethod
    def process_isbn(isbn):
        #only strip quotes if wsr, reg, or consignment number, or none
        if re.match('^wsr|^reg|^\d{2,4}-\d{1,4}$|n/a|none', isbn, re.I):
            isbn = re.sub('[\'\"]', '', isbn)
            price = None
        #strip quotes and whitespace. convert isbn10 to isbn13.
        #split isbn and price if it's an extended isbn
        else:
            isbn=re.sub('[\s\'\"\-]', '', isbn)
            price = None
            #note the checking for the first character of ean5 extension
            #if it's 5, it means price is in us dollars 0-99.99
            #otherwise, we need to do price ourself.
            if len(isbn) in (15,17,18):
                if isbn[-5] == '5':
                    price = float(isbn[-4:])/100
                isbn=isbn[:-5]
            if ( len(isbn)==10 and isbnlib.isValid(isbn)):
                isbn=isbnlib.convert(isbn)
        return isbn, price
 
    def lookup_by_isbn(self,number):
        isbn, price = self.process_isbn(number)
        print>>sys.stderr, isbn, price
        if (len(isbn)>0 and not re.match('^n(\s|/){0,1}a|none', isbn, re.I)):
            #first we check our database
            titles =  Title.select(Title.q.isbn==isbn)
            #print titles #debug
            self.known_title= False
            the_titles=list(titles)
            if len(the_titles) > 0:
                #print "in titles"
                self.known_title= the_titles[0]
                ProductName = the_titles[0].booktitle.format()
                authors=[]
                if len(the_titles[0].author) > 0:
                    authors = [x.authorName.format() for x in the_titles[0].author]
                authors_as_string = string.join(authors,',')
                categories=[]
                if len(the_titles[0].categorys) > 0:
                    #print len(the_titles[0].categorys)
                    #print the_titles[0].categorys
                    categories = [x.categoryName.format() for x in the_titles[0].categorys] 
                categories_as_string = string.join(categories,',')
                if len(the_titles[0].books) > 0:
                    ListPrice = max([x.listprice for x in the_titles[0].books])
                else:
                    ListPrice = 0
                Manufacturer = the_titles[0].publisher.format()
                Format=the_titles[0].type.format()
                Kind=the_titles[0].kind.kindName
                SpecialOrders=[tso.id for tso in Title.selectBy(isbn=isbn).throughTo.specialorder_pivots.filter(TitleSpecialOrder.q.orderStatus=='ON ORDER')]
                return {"title":ProductName,
                    "authors":authors,
                    "authors_as_string":authors_as_string,
                    "categories_as_string":categories_as_string,
                    "list_price":ListPrice,
                    "publisher":Manufacturer,
                    "isbn":isbn,
                    "format":Format,
                    "kind":Kind,
                    "known_title": self.known_title,
                    "special_order_pivots":SpecialOrders}
            else: #we don't have it yet
                #print "in isbn"
                sleep(1) # so amazon doesn't get huffy 
                ecs.setLicenseKey(amazon_license_key)
                ecs.setSecretAccessKey(amazon_secret_key)
                ecs.setAssociateTag(amazon_associate_tag)
                 
                #print "about to search", isbn, isbn[0]
                pythonBooks=[]
                 
                idType=''
                if len(isbn)==12:
                        idType='UPC'
                elif len(isbn)==13:
                        idType='EAN'
                try:
                        pythonBooks = ecs.ItemLookup(isbn,IdType= idType, SearchIndex="Books",ResponseGroup="ItemAttributes,BrowseNodes")
                except ecs.InvalidParameterValue:
                        pass
 
                #print pythonBooks
                if pythonBooks:
                    result={}
                    authors=[]
                    categories=[]
                    b=pythonBooks[0]
 
                    for x in ['Author','Creator', 'Artist', 'Director']:
                        if hasattr(b,x):
                            if type(getattr(b,x))==type([]):
                                authors.extend(getattr(b,x))
                            else:
                                authors.append(getattr(b,x))
                     
 
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
                                #print "hasansc"   
                                for i in item.Ancestors:
                                    bn.update(parseBrowseNodesInner(i))
                            if hasattr(item, 'Children'):
                                for i in item.Children:
                                    bn.update(parseBrowseNodesInner(i))
                                    #print "bn ", bn
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
        
 
                    categories=parseBrowseNodes(b.BrowseNodes)
                    categories_as_string = ', '.join(categories)
 
 
                    ProductName=""
                    if hasattr(b,'Title'):
                        ProductName=b.Title
 
                         
                    Manufacturer=""
                    if hasattr(b,'Manufacturer'):
                        Manufacturer=b.Manufacturer
 
                    ListPrice=""
                    if hasattr(b,'ListPrice'):
                        ListPrice=b.ListPrice.FormattedPrice.replace("$",'')
 
                    Format=''
                    if hasattr(b, "Binding"):
                        Format=b.Binding
                     
                    Kind=''
                    if b.ProductGroup=='Book':
                        Kind='books'
                    elif b.ProductGroup=='Music':
                        Kind='music'
                    elif b.ProductGroup in ('DVD', 'Video'):
                        Kind='film'
                     
                    return {"title":ProductName,
                        "authors":authors,
                        "authors_as_string":authors_as_string,
                        "categories_as_string":categories_as_string,
                        "list_price":ListPrice,
                        "publisher":Manufacturer,
                        "isbn":isbn,
                        "format":Format,
                        "kind":Kind,
                        "known_title": self.known_title,
                        "special_orders": []}
                else:
                    return []
                 
        
        else:
            return []
         
    def search_by_keyword(self, authorOrTitle=''):
        def database_gen(authorOrTitle=''):
            titles=[]
             
            #start out with the join clauses in the where clause list
            where_clause_list = []
            clause_tables=['book', 'author', 'author_title',]
            join_list=[LEFTJOINOn('title', 'book', 'book.title_id=title.id'), LEFTJOINOn(None, 'author_title', 'title.id=author_title.title_id'), LEFTJOINOn(None, 'author', 'author.id=author_title.author_id')]
             
            #add filter clauses if they are called for
            where_clause_list.append("(author.author_name RLIKE '%s' OR title.booktitle RLIKE '%s')" % (escape_string(authorOrTitle.strip()), escape_string(authorOrTitle.strip())))
            #AND all where clauses together
            where_clause=' AND '.join(where_clause_list)
            titles=[]
             
            #do search. 
            titles=Title.select( where_clause,join=join_list,clauseTables=clause_tables,distinct=True)
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
         
                for x in ['Author','Creator', 'Artist', 'Director']:
                    if hasattr(data,x):
                        if type(getattr(data,x))==type([]):
                            authors.extend(getattr(data,x))
                        else:
                            authors.append(getattr(data,x))
                 
         
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
                            #print "hasansc"   
                            for i in item.Ancestors:
                                bn.update(parseBrowseNodesInner(i))
                        if hasattr(item, 'Children'):
                            for i in item.Children:
                                bn.update(parseBrowseNodesInner(i))
                                #print "bn ", bn
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
                if hasattr(data,'Title'):
                    ProductName=data.Title
         
                     
                Manufacturer=""
                if hasattr(data,'Manufacturer'):
                    Manufacturer=data.Manufacturer
         
                ListPrice=""
                if hasattr(data,'ListPrice'):
                    ListPrice=data.ListPrice.FormattedPrice.replace("$",'')
         
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
                 
                return {"title":ProductName,
                    "authors":authors,
                    "authors_as_string":authors_as_string,
                    "categories_as_string":categories_as_string,
                    "list_price":ListPrice,
                    "publisher":Manufacturer,
                    "isbn":ISBN,
                    "format":Format,
                    "kind":Kind,
                    "known_title": None,}
         
            return (process_data(a) for a in ecs.ItemSearch(Keywords=authorOrTitle, SearchIndex='Books', ResponseGroup="ItemAttributes,BrowseNodes"))
         
        print>>sys.stderr, 'at ', authorOrTitle
        iter_array = [database_gen]
        #test if internet is up
        try:
            urllib2.urlopen('http://google.com', timeout=1)
        except:
            pass
        else:
            iter_array.append(amazon_gen)
         
        print>>sys.stderr, "iterarray ", iter_array
        for iter1 in iter_array:
            try:
                iter1=iter1(authorOrTitle)
            except IOError as err:
                print err
                yield
            except Exception as err:
                print err
                yield
            else:
                print iter1
                for element in iter1:
                    try:
                        yield element
                    except IOError:
                        print err
                        yield
                     
    def addToInventory(self,title="",status="STOCK",authors=[],publisher="",listprice="",ourprice='',isbn="",categories=[],distributor="",location='', location_id='',owner="",notes="",quantity=1,known_title=False,types='',kind_name="",kind=default_kind, extra_prices={}, tag='', num_copies=0, printlabel=False, special_orders=0):
        print>>sys.stderr, "GOT to addToInventory"
        if known_title:
            print>>sys.stderr, "known_title ", known_title
            if not known_title.booktitle:
                known_title.booktitle = title
            if not known_title.publisher:
                known_title.publisher = publisher
            if not known_title.type:
                known_title.type = types
        elif not(known_title):
            print>>sys.stderr, "unknown title"
            #add a title
            the_kinds=list(Kind.select(Kind.q.kindName==kind))
            kind_id = None
            if the_kinds:
                kind_id = the_kinds[0].id
            print>>sys.stderr, 'kind id is', kind_id
 
            #print>>sys.stderr, title
             
            title=title.encode('utf8', "backslashreplace")
            publisher=publisher
            #print>>sys.stderr, title, publisher
            known_title=Title(isbn=isbn, booktitle=title, publisher=publisher,tag=" ",type=types, kindID=kind_id)
            print>>sys.stderr, known_title
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
                print>>sys.stderr, "mmm... looks like you have multiple author of the sama name in your database..."
            for category in categories:
                Category(categoryName=category.encode("utf8", "backslashreplace"),title=known_title)
        #the_locations=list(Location.select(Location.q.locationName==location))
        #location_id=1
        #if the_locations:
        #    location_id = the_locations[0].id
        if not ourprice:
            ourprice=listprice
        print>>sys.stderr, "about to enter book loop"
        print>>sys.stderr, "location is", location
        print>>sys.stderr, "location_id is", location_id
        for i in range(int(quantity)): 
            print>>sys.stderr, "book loop"
            b=Book(title=known_title,status=status.encode("utf8", "backslashreplace"), distributor=distributor.encode('ascii', "backslashreplace"),listprice=listprice, ourprice=ourprice, location=int(location_id),owner=owner.encode("utf8", "backslashreplace"),notes=notes.encode("utf8", "backslashreplace"),consignmentStatus="")
#               b.extracolumns()
#~ #               for mp in extra_prices.keys():
#                   setattr(b,string.replace(mp," ",""),extra_prices[mp])
 
                 
    def getInventory(self,queryTerms):
        #print queryTerms
        keys=queryTerms.keys()
        print "keys are ", keys
         
        isbnSelect=""
        kindSelect=""
        statusSelect=""
        titleSelect=""
        authorSelect=""
        categorySelect=""
        clauseTables=[]
 
        if "kind" in keys: # joins suck, avoid if possible
            kind_map={}
            for k in [(x.kindName,x.id) for x in list(Kind.select())]:
                kind_map[k[0]]=k[1]
            try:
                kind_id=kind_map[queryTerms['kind']]
                kindSelect=Book.sqlrepr(AND(Field("book","title_id")==Field("title","id"), Field("title","kind_id")==kind_id))
            except: 
                pass
             
        if 'status' in keys:
            statusSelect=Book.sqlrepr(Field("book","status")==queryTerms["status"])
             
 
        if ('title' in keys) or ('authorName' in keys) or ('kind' in keys) or ('categoryName' in keys) or ('isbn' in keys):
            clauseTables.append('title') 
            #we are going to need to do a join 
 
            if 'title' in keys:
                titleSelect=Book.sqlrepr(AND(Field("book","title_id")==Field("title","id"), RLIKE(Field("title","booktitle"), queryTerms["title"])))
 
 
            if 'isbn' in keys:
                isbn, price = self.process_isbn(queryTerms['isbn'])
                print "isbn and price are ", isbn, price
                titleSelect=Book.sqlrepr(AND(Field("book","title_id")==Field("title","id"), Field("title","isbn")==isbn))
 
 
            if 'authorName' in keys:
                #authorSelect="""book.title_id = title.id AND author.title_id=title.id AND author.author_name RLIKE %s""" % (Book.sqlrepr(queryTerms["authorName"]))    
               authorSelect=Book.sqlrepr(AND(Field("book","title_id")==Field("title","id"), Field("author","id")==Field("author_title","author_id"), Field("title","id")==Field("author_title","title_id"), RLIKE(Field("author","author_name"), queryTerms["authorName"])))
               clauseTables.append('author')
               clauseTables.append('author_title')
             
            if 'categoryName' in keys:
                categorySelect="""book.title_id = title.id AND category.title_id=title.id AND category.category_name RLIKE %s""" % (Book.sqlrepr(queryTerms["categoryName"]))
                #categorySelect=Book.sqlrepr(AND(Field("book","title_id")==Field("title","id"), Field("category","title_id")==Field("title","id"), RLIKE(Field("category","category_name"), queryTerms["categoryName"])))
                clauseTables.append('category')
            # At this time, ubuntu install sqlobject 0.6.1 if apt-get install python2.4-sqlobject,
            # which make the search crash, since the distinct attribute is defined somewhere after 0.6.1 
        try:
            books=Book.select(
                string.join([term for term in [statusSelect,titleSelect,authorSelect,kindSelect,categorySelect] if term !=""]," AND "),
                clauseTables=clauseTables,
                distinct=True    )
        except TypeError:
            books=Book.select(
                string.join([term for term in [statusSelect,titleSelect,authorSelect,kindSelect,categorySelect] if term !=""]," AND "),
                clauseTables=clauseTables   )
 
        results={}
        i=1
        for b in books:
            theTitle=b.title.booktitle
            authorString=string.join([a.authorName for a in b.title.author],",")
            categoryString=string.join([c.categoryName for c in b.title.categorys],",")
            results[i]=(string.capitalize(theTitle),
                        authorString, 
                        b.listprice  if b.listprice is not None else '',
                        b.title.publisher if b.title.publisher is not None else '',
                        b.status if b.status is not None else'',
                        b.title.isbn,
                        b.distributor if b.distributor is not None else '',
                        b.location.locationName if b.location is not None else '',
                        b.notes if b.notes is not None else '',
                        b.id,
                        b.title.kind and b.title.kind.kindName if b.title.kind is not None else '',
            categoryString,
            b.title.type if b.title.type is not None else '')
        return results
 
    
