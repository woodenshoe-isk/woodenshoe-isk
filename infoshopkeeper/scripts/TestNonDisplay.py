from sqlobject.sqlbuilder import RLIKE
from objects.title import Title

import lxml
from lxml import html, cssselect

import webtest
from wsgiapp_local import application


try:
    theapp=webtest.TestApp(application)
except:
    pass

titles=Title.select(RLIKE(Title.q.isbn, '^[0-9]{9}[0-9xX]$'))
titles_that_display, titles_that_dont_display, titles_that_dont_even_fetch=(0, [], [])

for title in titles:
    try:
        response=theapp.get('/search', {'id':title.id})
        lx_htm=lxml.html.fromstring(response.text)        
        if lx_htm.cssselect('tbody tr td').__len__() > 1:
            titles_that_display += 1
        else:
            titles_that_dont_display.append(title.id)
        
    except Exception as e:
        print(e)
        titles_that_dont_even_fetch.append(title.id)
print("Number of titles that don't fetch: ", titles_that_dont_even_fetch.__len__())
print("Number of titles that don't display: ", titles_that_dont_display.__len__())
print("Number of titles that display: ", titles_that_display)

print("Titles that don't display are: ", titles_that_dont_display)
print("Titles that don't fetch are: ", titles_that_dont_even_fetch)

diagnostic_dict={}
for t in titles_that_dont_display:
    t_rec=Title.get(t)
    rm_dirty=False
    if not list(t_rec.books):
        book_list=diagnostic_dict.get('book', [])
        book_list.append(t)
        diagnostic_dict['book']=book_list
        rm_dirty=True
    if not list(t_rec.author):
        author_list=diagnostic_dict.get('author', [])
        author_list.append(t)
        diagnostic_dict['author']=author_list
        rm_dirty=True
    if not list(t_rec.categorys):
        result_list=diagnostic_dict.get('category', [])
        result_list.append(t)
        diagnostic_dict['category']=result_list
    try:
        t_rec.safe('booktitle')
    except:
        result_list=diagnostic_dict.get('safe_booktitle', [])
        result_list.append(t)
        diagnostic_dict['safe_booktitle']=result_list
        rm_dirty=True
    if not t_rec.authors_as_string():
        result_list=diagnostic_dict.get('authors_as_string', [])
        if not diagnostic_dict.get('author', []).count(t):
            result_list.append(t)
            diagnostic_dict['authors_as_string']=result_list
            rm_dirty=True
    if not t_rec.type:
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
                
    if rm_dirty:
        titles_that_dont_display.remove(t)
        
if diagnostic_dict.get('book'):
    print("Titles that don't have books are: ", diagnostic_dict['book'])
if diagnostic_dict.get('author'):
    print("Titles that don't have authors are: ", diagnostic_dict['author'])
if diagnostic_dict.get('category'):
    print("Titles that don't have categories are: ", diagnostic_dict['category'])
if diagnostic_dict.get('safe_booktitle'):
    print("Titles whose booktitle doesn't display safely are: ", diagnostic_dict['safe_booktitle'])
if diagnostic_dict.get('authors_as_string'):
    print("Titles whose authors don't display safely as string are: ", diagnostic_dict['authors_as_string'])
if diagnostic_dict.get('type'):
    print("Titles without type are: ", diagnostic_dict['type'])
if diagnostic_dict.get('distributors_as_string'):
    print("Titles without distributors as string are: ", diagnostic_dict['distributors_as_string'])
if diagnostic_dict.get('publisher'):
    print("Titles without publisher are: ", diagnostic_dict['publisher'])
if titles_that_dont_display:
    print("The remainder of problem tiles are: ", titles_that_dont_display)
   
    

