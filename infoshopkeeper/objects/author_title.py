from tools import db

# from objects.author import Author
# from objects.title import Title
from sqlobject import *
from objects.SQLObjectWithFormGlue import SQLObjectWithFormGlue


class AuthorTitle(SQLObjectWithFormGlue):
    author = ForeignKey("Author")
    title = ForeignKey("Title")

    class sqlmeta:
        fromDatabase = True
        table = "author_title"
