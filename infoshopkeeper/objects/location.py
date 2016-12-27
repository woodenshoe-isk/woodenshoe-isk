import sys

from sqlobject import *
from tools import db
from .SQLObjectWithFormGlue import SQLObjectWithFormGlue


class Location(SQLObjectWithFormGlue):
	class sqlmeta:
		fromDatabase = True




