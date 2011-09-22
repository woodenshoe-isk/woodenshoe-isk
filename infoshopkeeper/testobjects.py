from etc import *

from sqlobject import *
from sqlobject.sqlbuilder import *

#Set up db connection
connection = connectionForURI('mysql://%s:%s@%s:3306/%s?debug=1&logger=MyLogger&loglevel=debug&use_unicode=1&charset=utf8' % (dbuser,dbpass,dbhost,dbname))
sqlhub.processConnection = connection


class Title(SQLObject):
    class sqlmeta:
        fromDatabase = True
    booktitle=UnicodeCol(default=None)
    books = MultipleJoin('Book')
    author = RelatedJoin('Author', intermediateTable='author_title',createRelatedTable=True)
    categorys = MultipleJoin('Category')
    kind = ForeignKey('Kind')
    listTheseKeys=('kind')
    

class Author(SQLObject):
    class sqlmeta:
        fromDatabase = True

    authorName=UnicodeCol(default=None)
    title = RelatedJoin('Title', intermediateTable='author_title',createRelatedTable=True)
