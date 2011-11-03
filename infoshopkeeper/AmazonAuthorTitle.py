from objects.SQLObjectWithFormGlue import SQLObjectWithFormGlue

from ecs import *
from etc import *

from sqlobject import *
from sqlobject.sqlbuilder import *

import time
from Queue import Queue, Empty
from threading import Thread

import re

import logging
import logging.handlers

import readline

import shelve

import pdb

my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(logging.DEBUG)

# Add the log message handler to the logger
handler = logging.handlers.RotatingFileHandler("SQLObject.log", maxBytes=20, backupCount=5)
my_logger.addHandler(handler)

#Set up db connection
connection = connectionForURI('mysql://%s:%s@%s:3306/%s?debug=1&logger=MyLogger&loglevel=debug&use_unicode=1&charset=utf8' % (dbuser,dbpass,dbhost,dbname))
sqlhub.processConnection = connection

#recursively do a frozenset on a list of lists
def freeze(list):
    try:
        return frozenset(list)
    except TypeError, e:
        return frozenset(map(freeze, list))


def main():
    amazonQueue = MyQueue()
    addExtraInfoQueue=MyQueue()
    comparisonQueue= MyQueue()
    guiQueue = MyQueue()
    
    #Get all valid isbns and put them in a queue for amazon
    for x in connection.queryAll(connection.sqlrepr(sqlbuilder.Select(Title.q.isbn, where=(RLIKE(Title.q.isbn, '^[0-9]{9}[0-9xX]{1}$') & (Title.q.kindID==1)), groupBy=Title.q.isbn, limit=200))):
        amazonQueue.put({'isbn':x[0]})
    
    #We've finished all isbns & aren't just blocking for input
    amazonQueue.setDoneWaiting(True)
    
    #Get info for each isbn from amazon
    amazonThread=AmazonThread(amazonQueue, addExtraInfoQueue, comparisonQueue)
    amazonThread.start()
    
    #Get category and item format while we have the amazon info record
    #We do this for each item because we don't have this stuff yet
    addExtraInfoThread=AddExtraInfoThread(addExtraInfoQueue)
    addExtraInfoThread.start()
    
    #Compare the info  for each item from amazon with our db info
    #if there's a conflict, put on guiQueue so we can resolve it
    comparisonThread=ComparisonThread(comparisonQueue, guiQueue)
    comparisonThread.start()
    
    keepRunning=True
    amazonQueue.join()
    #gui loop for dealing with corrections
    while keepRunning:
        try:
            correction1 = guiQueue.get(False)
            
            #print title if no correction
            if len(correction1['booktitleList'])==1:
                print correction1['booktitleList'][0]
            #add titles to readline
            #ask which one to keep
            else:
                readline.clear_history()
                for i, x in enumerate(correction1['booktitleList']):
                    print '%s. %s' % (i, x)
                    try:
			readline.add_history(x)
		    except:
			break
                inputline=raw_input("Which Title do you want to keep?\n")
                result=''
                #break on quit.
                #accepts the number of the right title
                #also lets you use the readline history to page & edit yourself
                if inputline=='q':
                    keepRunning=False
                    break
                else:
                    try:
                        result=correction1['booktitleList'][int(inputline)]
                    except ValueError:
                        result=inputline
                print 'You entered: %s' % result
                for t in correction1['ourTitles']:
                    t.set(booktitle=result)
            
            #if author does't need correction, just print it out
            if len(correction1['authorList'])==1:
                print correction1['authorList'][0]
            #otherwise add authors to readline history and print them out
            else:
                readline.clear_history()
                #for each correction, turn candidate array into a tab
                #delimited string for display
                for i, x in enumerate(correction1['authorList']):
                    authorString=''
                    print '%d: ' % i,
                    for y in x:
                        authorString=authorString + y + '\t'
                        print y + '\t',
                    else:
                        authorString=authorString[0:-1]
                        print '\n',
		    print type(authorString)
                    try:
			readline.add_history(authorString.encode("utf-8"))
		    except:
			break
                #number of choice is fine, else use readline hist for editing or choosing
                inputline=raw_input("Which set of authors do you want to keep?\n(Separate authors by tabs)\n")
                result=[]
                #quit if choice is q
                if inputline=='q':
                    keepRunning=False
                    break
                #if input is number, add the array we already had.
                #if input is string, reconstitute the array from the tabbed author list
                else:
                    try:
                        result=correction1['authorList'][int(inputline)]
                    except ValueError:
                        result=inputline.split('\t')
                #add authors to title
                for a in result:
		    print a
                    #add author to author table if not there already
                    if len(list(Author.selectBy(authorName=a)))==0:
                         Author(authorName=a)
		    elif Author.selectBy(authorName=a)[0].authorName.lower() == a.lower():
			author1=Author.selectBy(authorName=a)[0]
			print author1
			author1.authorName = a+'12345'
			print author1
			author1.authorName = a
			print author1
                    for t in correction1['ourTitles']:
                        #connect author to title
                        if a not in t.author:
                            t.addAuthor(Author.selectBy(authorName=a)[0])
			print t.author
			print result
                        #remove authors from title that aren't in result
                for a1 in t.author:
                    if a1.authorName not in result:
                        t.removeAuthor(a1)
		print t.author
                print 'You entered: %s' % result
                
	    ''' #print publisher if no correction
            if len(correction1['publisherList'])==1:
                print correction1['publisherList'][0]
            #add publisher to readline
            #ask which one to keep
            else:
                readline.clear_history()
                for i, x in enumerate(correction1['publisherList']):
                    print '%s. %s' % (i, x)
                    readline.add_history(x)
                inputline=raw_input("Which Publisher do you want to keep?\n")
                result=''
                #break on quit.
                #accepts the number of the right publisher (try)
                #also lets you use the readline history to page & edit yourself (except)
                if inputline=='q':
                    keepRunning=False
                    break
                else:
                    try:
                        result=correction1['publisherList'][int(inputline)]
                    except ValueError:
                        result=inputline
                print 'You entered: %s' % result
                for t in correction1['ourTitles']:
                    t.set(publisher=result)'''
                
            guiQueue.task_done()
        except Empty:
	    print "quiqueue ", guiQueue.isDoneWaiting()
            if guiQueue.isDoneWaiting():
                keepRunning=False
            time.sleep(2)

    guiQueue.join()
   

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


class Category(SQLObjectWithFormGlue):
    class sqlmeta:
        fromDatabase = True

    categoryName=UnicodeCol(default=None)
    title = ForeignKey('Title')


#A queue w/ a semaphore for programmatic signalling of when we're really done
class MyQueue(Queue):
    def __init__(self):
        Queue.__init__(self)
        self.doneWaiting=False

    def isDoneWaiting(self):
        return self.doneWaiting
        
    def setDoneWaiting(self, doneWaiting):
        self.doneWaiting=doneWaiting
   

class AmazonThread(Thread):
    def __init__(self, amazonQueue, addExtraInfoQueue, comparisonQueue):
        Thread.__init__(self)

        setLicenseKey(amazon_license_key)
        setSecretAccessKey(amazon_secret_key)
        setAssociateTag(amazon_associate_tag)

        self.amazonQueue = amazonQueue
        self.comparisonQueue = comparisonQueue
        self.addExtraInfoQueue = addExtraInfoQueue
        self.keepRunning=True

    def getFromAmazon(self, title1):
        #oddly enough, sometimes book is not first ean/isbn returned
        #not sure if its due to the alternate ASIN id
        #basically we're checking to make sure that the first item isn't
        #patio furniture (really), but assume the first product of the proper
        #type is the right one.
        try:
            amazonItems=ItemLookup(title1['isbn'],  SearchIndex="Books", IdType="ISBN", ResponseGroup="ItemAttributes,BrowseNodes")
            
            for x in list(amazonItems):
                if x.ProductGroup in ['Book', 'DVD', 'Music', 'Video']:
                    amazonItem=x
                    break
            else:
                for x in list(amazonItems):
                    print x.ProductGroup
                    raise InvalidParameterValue
            return amazonItem
        except InvalidParameterValue:
            pass
    
    def run(self):
        while self.keepRunning:
            #get info for isbn from amazon.
            #put a copy in addExtraInfoQueue so we can get more info
            #put a copy in comparisonQueue so we can compare
            #our title/author info w/ amazon's
            try:
                title1 = self.amazonQueue.get(False)
		try:
			amazonTitle1=self.getFromAmazon(title1)
			self.comparisonQueue.put({'amazonItem':amazonTitle1})
			self.addExtraInfoQueue.put({'amazonItem':amazonTitle1})
		except:
			pass
		print self.amazonQueue.qsize()
                self.amazonQueue.task_done()
            except Empty:
                #if we've made it through all isbns & aren't
                #just waiting on input, then let thread die
                if self.amazonQueue.isDoneWaiting():
                    self.keepRunning=False
                    self.comparisonQueue.setDoneWaiting(True)
            #sleep for one second so amazon doesn't get mad.
            #we're only allowed one request per second for free
            time.sleep(1)


class AddExtraInfoThread(Thread):
    def __init__(self, addExtraInfoQueue):
        Thread.__init__(self)

        self.addExtraInfoQueue = addExtraInfoQueue
        self.keepRunning=True
        #
        self.regexp=re.compile('.*(?=Paperback)', re.I)
        

    def listfunc(self, x):
        try:
            it=x.__iter__()
            return [self.listfunc(y) for y in x]
        except:
            return x

    def processTitle(self, amazonItem, titleList):
        for title in titleList:
            #edit format. kill "mass market" or "trade" from paperback
            ourFormat=self.regexp.sub("", amazonItem.Binding)
            title.format=ourFormat
	    title.publisher=amazonItem.Publisher

	    def listCategories(browsenodes):
			def parseBrowseNode( browseNode ):
				if hasattr(browseNode, 'Ancestors'):
					if len(browseNode.Ancestors) > 0:
						for x in  parseBrowseNode( browseNode.Ancestors.pop()):
							yield x
				try:
				    yield browseNode.Name
				except:
				    pass
				if hasattr(browseNode, 'Children'):
					if len(browseNode.Children) > 0:
						for x in browseNode.Children:
							yield x.Name
			categoryList=[]
			for node in browsenodes:
				categoryList.extend( list(parseBrowseNode( node )))
			return categoryList

                    #~ for category in b.Subjects:
                       #~ categories.append(category)
	    categories=listCategories(amazonItem.BrowseNodes)
            for item in categories:
                if len(list(Category.selectBy(title=title.id, categoryName=item)))==0:
                    Category(title=title, categoryName=item)
            
    def run(self):
        while self.keepRunning:
            try:
                amazonTitle1 = self.addExtraInfoQueue.get(False)
                titleList1=Title.selectBy(isbn=amazonTitle1['amazonItem'].ISBN)
                self.processTitle(amazonTitle1['amazonItem'], titleList1)
                self.addExtraInfoQueue.task_done()
                time.sleep(1)
            except Empty:
                if self.addExtraInfoQueue.isDoneWaiting():
                    self.keepRunning=False
                time.sleep(1)


class ComparisonThread(Thread):
    def __init__(self, comparisonQueue, guiQueue):
        Thread.__init__(self)

        self.comparisonQueue = comparisonQueue
        self.guiQueue = guiQueue
        self.keepRunning=True
        
        self.titleSubRexp=re.compile('\s?\(.*Edition\)\s?')
        self.authorSubRexp= re.compile(r"(?:et.? al.? ?)|(?:\(ed.?\) ?)")


    def listfunc(self, x):
        try:
            it=x.__iter__()
            return [self.listfunc(y) for y in x]
        except:
            return x


    def processTitle(self, item, titleList):
        amazonItem=item['amazonItem']
        bookTitleList=[x.booktitle for x in titleList]
        
        corrections=dict(bookTitleDirty=False, authorDirty=False, publisherDirty=False)
        
        amazonTitle=''
        if not hasattr(amazonItem, 'Title'):
            return
        else:
            amazonTitle=amazonItem.Title
            #reformat title. Eliminate edition info as part of title
            amazonTitle=self.titleSubRexp.sub('', amazonTitle)
        
        #add amazonTitle to booktitleList.
        #uniquify list & mark as dirty if corrections are needed
        bookTitleList.append(amazonTitle)
        uniqueBookTitleList=freeze(bookTitleList)
        if (uniqueBookTitleList.__len__()>1):
            corrections['bookTitleDirty']=True
        
        #get list of publishers. add amazon's publisher to list
        publisherList=[x.publisher for x in titleList]
        amazonPublisher=''
        if hasattr(amazonItem, 'Publisher'):
            amazonPublisher=amazonItem.Publisher
        publisherList.append(amazonPublisher)
        
        #uhiquify puglisher & mark as dirty if list > 1
        uniquePublisherList=freeze(publisherList)
        if (uniquePublisherList.__len__()>1):
            corrections['publisherDirty']=True
        amazonAuthor=[]
        #generate a list of authors.
        if hasattr(amazonItem, 'Author'):
            #amazon returns single authors as string
            if (type(amazonItem.Author) is types.UnicodeType):
                amazonAuthor.append(amazonItem.Author)
            #but multiple authors as lis of strings
            else:
                amazonAuthor=amazonItem.Author
        
        #do the same for creator
        amazonCreator=[]
        if hasattr(amazonItem, 'Creator'):
            if (type(amazonItem.Creator) is types.UnicodeType):
                    amazonCreator.append(amazonItem.Creator)
            else:
                amazonCreator=amazonItem.Creator

        #some books have only creator, some have both
        #anyway, add creator if it's not there already        
        for c in amazonCreator:
            if c not in amazonAuthor:
                amazonAuthor.append(c)
        
        #remove editor, et. al. from author fields
        amazonAuthor=[self.authorSubRexp.sub("", x) for x in amazonAuthor]
        
        #get authors from database & add the amazon authors
        authorList=[[a.authorName for a in t.author]  for t in titleList]
        authorList.append(amazonAuthor)
        
        #uniquify this list of lists
        #we lose author order on this
        #if we end up with a list of author lists thats larger than one, mark
        uniqueAuthorList=freeze(authorList)
        if (uniqueAuthorList.__len__() > 1):
           corrections['authorDirty']=True
        
        #if corrections are needed, add to guiQueue
        if (corrections['authorDirty'] or corrections['bookTitleDirty'] or corrections['publisherDirty']):
            corrections['authorList'] = self.listfunc(uniqueAuthorList)
            corrections['booktitleList'] = list(uniqueBookTitleList)
            corrections['publisherList']=list(uniquePublisherList)
            corrections['ourTitles'] = titleList
            self.guiQueue.put(corrections)
            
            
    def run(self):
        while self.keepRunning:
            try:
                amazonTitle1 = self.comparisonQueue.get(False)
                titleList1=Title.selectBy(isbn=amazonTitle1['amazonItem'].ISBN)
                self.processTitle(amazonTitle1, titleList1)
                self.comparisonQueue.task_done()
            except Empty:
                #make sure we are really done & not just waiting  on input
                if self.comparisonQueue.isDoneWaiting():
                    self.keepRunning=False
                    self.guiQueue.setDoneWaiting(True)
            time.sleep(1)


if __name__ == '__main__':
    main()
