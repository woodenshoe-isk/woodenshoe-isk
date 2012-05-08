from time import time,asctime,localtime,sleep
import types,string

import ecs
from etc import amazon_license_key,amazon_secret_key, amazon_associate_tag
from objects.title import Title
from objects.book import Book
from objects.author import Author
from objects.category import Category
from objects.kind import Kind
from objects.location import Location
from upc import upc2isbn
import re
from sqlobject.sqlbuilder import Field, RLIKE, AND

class inventory:
    def __init__(self):
        x=1
       
        
    def lookup_by_isbn(self,number):
        isbn=""
        number=re.sub("^([\'\"])(.*)\\1$", '\\2', number)
        #print "number is now: ", number
        if len(number)>=9:
            number=re.sub("[-\s]", '', number)
        #print "number is now: ", number
        if len(number)==13 or len(number)==18:
            isbn=upc2isbn(number)
        else:
            isbn=number
        #print "NUMBER was " +number+ ",ISBN was "+isbn
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
                    ListPrice = the_titles[0].books[0].listprice
                else:
                    ListPrice = 0
                Manufacturer = the_titles[0].publisher.format()
                Format=the_titles[0].type.format()
                Kind=the_titles[0].kind.kindName
                return {"title":ProductName,
                    "authors":authors,
                    "authors_as_string":authors_as_string,
                    "categories_as_string":categories_as_string,
                    "list_price":ListPrice,
                    "publisher":Manufacturer,
                    "isbn":isbn,
                    "format":Format,
                    "kind":Kind,
                    "known_title": self.known_title}
            else: #we don't have it yet
                #print "in isbn"
                sleep(1) # so amazon doesn't get huffy 
                ecs.setLicenseKey(amazon_license_key)
                ecs.setSecretAccessKey(amazon_secret_key)
                ecs.setAssociateTag(amazon_associate_tag)
                
                #print "about to search", isbn, isbn[0]
                pythonBooks=[]
                try:
                    pythonBooks = ecs.ItemLookup(isbn,IdType="ISBN",SearchIndex="Books",ResponseGroup="ItemAttributes,BrowseNodes")
                except ecs.InvalidParameterValue:
                    pass
                #print pythonBooks
                if pythonBooks:
                    result={}
                    authors=[]
                    categories=[]
                    b=pythonBooks[0]

                    for x in ['Author','Creator']:
                        if hasattr(b,x):
                            if type(getattr(b,x))==type([]):
                                authors.extend(getattr(b,x))
                            else:
                                authors.append(getattr(b,x))
                    

                    authors_as_string = string.join(authors,',')
 
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
                    categories_as_string = string.join(categories,',')                   

                    categories=parseBrowseNodes(b.BrowseNodes)
                    categories_as_string = string.join(categories,',')
                    #print categories, categories_as_string


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
                    
                    Kind='books'
                    
                    return {"title":ProductName,
                        "authors":authors,
                        "authors_as_string":authors_as_string,
                        "categories_as_string":categories_as_string,
                        "list_price":ListPrice,
                        "publisher":Manufacturer,
                        "isbn":isbn,
                        "format":Format,
                        "kind":Kind,
                        "known_title": self.known_title}
                else:
                    return []
                
       
        else:
            return []
        
    def lookup_by_upc(self,upc):

        if len(upc)>0:
            #first we check our database
            titles =  Title.select(Title.q.isbn==upc)
            #print titles #debug
            self.known_title= False
            the_titles=list(titles)
            if len(the_titles) > 0:
                self.known_title= the_titles[0]
                ProductName = the_titles[0].booktitle
                authors = [x.authorName for x in the_titles[0].authors]
                authors_as_string = string.join(authors,',')
                categories = [x.categoryName for x in the_titles[0].categorys]
                categories_as_string = string.join(categories,',')
                if len(the_titles[0].books) > 0:
                    ListPrice = the_titles[0].books[0].listprice
                else:
                    ListPrice = 0
                Manufacturer = the_titles[0].publisher
                
            else: #we don't have it yet
                sleep(1) # so amazon doesn't get huffy 
                ecs.setLicenseKey(amazon_license_key)
                ecs.setSecretAccessKey(amazon_secret_key)
                ecs.setAssociatTag(amazon_associate_tag)
                pythonItems = ecs.searchByUPC(upc)
                if pythonItems:
                    result={}
                    authors=[]
                    author_object="none"
                    categories=[]
                    b=pythonItems[0]
                    try:
                        author_object=b.Artists.Artist
                    except AttributeError:
                        author_object="none"
                    if type(author_object) in types.StringTypes:
                        authors.append(author_object)
                    else: 
                        authors=author_object
                    authors_as_string = string.join(authors,',')

                    for category in b.BrowseNode:
                        categories.append(category.BrowseName)

                    categories_as_string = string.join(categories,',')
                 
                    ProductName=""
                    try:
                        if b.ProductName:
                            ProductName=b.ProductName
                    except AttributeError:
                        x=1
                        
                    Manufacturer=""
                    try:
                        if b.Manufacturer:
                            Manufacturer=b.Manufacturer
                    except AttributeError:
                        x=1

                    ListPrice=""
                    try:
                        if b.ListPrice:
                            ListPrice=b.ListPrice
                    except AttributeError:
                        x=1

                    ReleaseDate=""
                    try:
                        if b.ReleaseDate:
                            ReleaseDate=b.ReleaseDate
                    except AttributeError:
                        x=1
                    
            return {"title":ProductName,
                    "authors":authors,
                    "authors_as_string":authors_as_string,
                    "categories_as_string":categories_as_string,
                    "list_price":ListPrice,
                    "publisher":Manufacturer,
                    "isbn":upc,
                    "known_title": self.known_title}


    def addToInventory(self,title="",status="STOCK",authors=[],publisher="",listprice="",ourprice='',isbn="",categories=[],distributor="",location="",owner="",notes="",quantity=1,known_title=False,types='',kind_name="",kind='', extra_prices={}, tag='', num_copies=0, printlabel=False):
        print "GOT to addToInventory"
        if not(known_title):
            print "unknown title"
            #add a title
            the_kinds=list(Kind.select(Kind.q.kindName==kind))
            kind_id = None
            if the_kinds:
                kind_id = the_kinds[0].id
            print kind_id

            #print title
            
            title=title
            publisher=publisher
            #print title, publisher
            known_title=Title(isbn=isbn, booktitle=title, publisher=publisher,tag=" ",type=types, kindID=kind_id)
            print known_title
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
                print "mmm... looks like you have multiple author of the sama name in your database..."
            for category in categories:
                Category(categoryName=category.encode("utf8", "backslashreplace"),title=known_title)
        the_locations=list(Location.select(Location.q.locationName==location))
        location_id=1
        if the_locations:
            location_id = the_locations[0].id
        if not ourprice:
            ourprice=listprice
        for i in range(int(quantity)): 
            #print "book loop"
            b=Book(title=known_title,status=status.encode("utf8", "backslashreplace"), distributor=distributor.encode('ascii', "backslashreplace"),listprice=listprice, ourprice=ourprice, location=location_id,owner=owner.encode("utf8", "backslashreplace"),notes=notes.encode("utf8", "backslashreplace"),consignmentStatus="")
#               b.extracolumns()
#~ #               for mp in extra_prices.keys():
#                   setattr(b,string.replace(mp," ",""),extra_prices[mp])



                
    def getInventory(self,queryTerms):
        #print queryTerms
        keys=queryTerms.keys()
        
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
                titleSelect=Book.sqlrepr(AND(Field("book","title_id")==Field("title","id"), Field("title","isbn")==queryTerms["isbn"]))


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
        #~ for b in books:
            #~ theTitle=b.title.booktitle.format()
            #~ authorString=string.join([a.authorName.format() for a in b.title.author],",")
            #~ categoryString=string.join([c.categoryName.format() for c in b.title.categorys],",")
            #~ results[i]=(string.capitalize(theTitle),
                        #~ authorString, 
                        #~ b.listprice  if b.listprice is not None else '',
                        #~ b.title.publisher.format() if b.title.publisher is not None else '',
                        #~ b.status.format() if b.status is not None else'',
                        #~ b.title.isbn,
                        #~ b.distributor.format() if b.distributor is not None else '',
            #~ b.location.locationName.format() if b.location is not None else '',
                        #~ b.notes.format() if b.notes is not None else '',
                        #~ b.id,
                        #~ b.title.kind and b.title.kind.kindName if b.title.kind is not None else '',
            #~ categoryString,
            #~ b.title.type if b.title.type is not None else '')

            i=i+1                
        #print "results are ", results
        return results

    
