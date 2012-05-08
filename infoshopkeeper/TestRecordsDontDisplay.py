import sys

from sqlobject.sqlbuilder import RLIKE

import lxml
from lxml import html, cssselect

import webtest
from wsgiapp_local import application

from etc import *
from ecs import *
from objects.title import Title
from objects.author import Author
from objects.category import Category

setLicenseKey(amazon_license_key)
setSecretAccessKey(amazon_secret_key)
setAssociateTag(amazon_associate_tag)

#make sure we're in production database
dbname='infoshopkeeper'
try:
    theapp=webtest.TestApp(application)
except:
    pass

titles=Title.select(RLIKE(Title.q.isbn, '^[0-9]{10}[0-9xX]$|^[0-9]{13}$'))
titles_that_display, titles_that_dont_display, titles_that_dont_even_fetch=(0,[],[])

for title in titles:
    try:
        response=theapp.get('/search', {'id':title.id})
        lx_htm=lxml.html.fromstring(response.text)        
        if lx_htm.cssselect('tbody tr td').__len__() > 1:
            titles_that_display += 1
        else:
            titles_that_dont_display.append(title.id)
        
    except Exception as e:
        print e
        titles_that_dont_even_fetch.append(title.id)
print "Number of titles that don't fetch: ", titles_that_dont_even_fetch.__len__()
print "Number of titles that don't display: ", titles_that_dont_display.__len__()
print "Number of titles that display: ", titles_that_display

print "Titles that don't display are: ", titles_that_dont_display
print "Titles that don't fetch are: ", titles_that_dont_even_fetch

diagnostic_dict={}
for t in titles_that_dont_display:
    t_rec=Title.get(t)
    rm_dirty=False
    if not list(t_rec.books):
        book_list=diagnostic_dict.get('book', [])
        book_list.append(t)
        diagnostic_dict['book']=book_list
        rm_dirty=True
    if (hasattr(t_rec, 'author') and not t_rec.authors_as_string()):
        author_list=diagnostic_dict.get('authors_as_string', [])
        author_list.append(t)
        diagnostic_dict['authors_as_string']=author_list
        rm_dirty=True
    if not list(t_rec.categorys):
        result_list=diagnostic_dict.get('category', [])
        result_list.append(t)
        diagnostic_dict['category']=result_list
        rm_dirty=True
    try:
        t_rec.safe('booktitle')
    except:
        result_list=diagnostic_dict.get('safe_booktitle', [])
        result_list.append(t)
        diagnostic_dict['safe_booktitle']=result_list
        rm_dirty=True
    if not hasattr(t_rec, 'author'):
        result_list=diagnostic_dict.get('author', [])
        if not diagnostic_dict.get('author', []).count(t):
            result_list.append(t)
            diagnostic_dict['author']=result_list
            rm_dirty=True
    try:
        t_rec.type
    except:
        result_list=diagnostic_dict.get('type', [])
        result_list.append(t)
        diagnostic_dict['type']=result_list
        rm_dirty=True
    if not t_rec.distributors_as_string():
        if t_rec.distributors_as_string()!='':
            result_list=diagnostic_dict.get('distributors_as_string', [])
            result_list.append(t)
            diagnostic_dict['distributors_as_string']=result_list
            rm_dirty=True
    if not t_rec.safe('publisher'):
        result_list=diagnostic_dict.get('publisher', [])
        result_list.append(t)
        diagnostic_dict['publisher']=result_list
        rm_dirty=True            
    try:
        t_rec.kind
    except:
        result_list=diagnostic_dict.get('kind', [])
        result_list.append(t)
        diagnostic_dict['kind']=result_list
        rm_dirty=true
    if rm_dirty:
        titles_that_dont_display.remove(t)
        
if diagnostic_dict.get('book'):
    print "Titles that don't have books are: ", diagnostic_dict['book']
if diagnostic_dict.get('author'):
    print "Titles that don't have authors are: ", diagnostic_dict['author']
if diagnostic_dict.get('category'):
    print "Titles that don't have categories are: ", diagnostic_dict['category']
if diagnostic_dict.get('safe_booktitle'):
    print "Titles whose booktitle doesn't display safely are: ", diagnostic_dict['safe_booktitle']
if diagnostic_dict.get('authors_as_string'):
    print "Titles whose authors don't display safely as string are: ", diagnostic_dict['authors_as_string']
if diagnostic_dict.get('type'):
    print "Titles without type are: ", diagnostic_dict['type']
if diagnostic_dict.get('distributors_as_string'):
    print "Titles without distributors as string are: ", diagnostic_dict['distributors_as_string']
if diagnostic_dict.get('publisher'):
    print "Titles without publisher are: ", diagnostic_dict['publisher']
if diagnostic_dict.get('kind'):
    print 'Titles without kind are: ', diagnostic_dict['kind']
if titles_that_dont_display:
    print "The remainder of problem tiles are: ", titles_that_dont_display
   
sys.exit(0) 

def get_authors_from_amazon(auth_missing=[]):
    for t in auth_missing:
        t1=Title.get(t)
        try:
            amazonIter=ItemLookup(t1.isbn, ResponseGroup="ItemAttributes")
            amazonResults=amazonIter.next()
            if type( getattr(amazonResults, 'Author', False)) == type(u''):
                auth= [ getattr(amazonResuts, 'Author', None) ]
            else:
                auth=getattr( amazonResults, 'Author', [])
            print auth
            if type( getattr(amazonResults,'Creator', False)) == type(u''):
                auth.extend([ getattr(amazonResuts, 'Creator', None) ])
            else:
                auth.extend(getattr( amazonResults, 'Creator', []))
            au_rec=''                
            for au in auth:
                try:
                    Author(authorName=au)           
                except Exception: 
                    pass
                au_rec=Author.selectBy(authorName=au)[0]
                print au_rec
                t1.addAuthor(au_rec)
                print t1.author
        except Exception as e:
            print e
             
def get_categories_from_amazon( category_missing=[]):
    for t in auth_missing:
        t1=Title.get(t)
        try:
            amazonIter=ItemLookup(t1.isbn, ResponseGroup="ItemAttributes, BrowseNodes")
            amazonResults=amazonIter.next()
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
        except Exception as e:
            print e