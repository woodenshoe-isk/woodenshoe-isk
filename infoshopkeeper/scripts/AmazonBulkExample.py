from config.config import configuration
from ecs import *
from objects.book import *
from objects.images import *
from objects.author import *
from objects.category import *

from sqlobject.sqlbuilder import *
import time
import traceback


setLicenseKey(configuration.get('amazon_license_key'))
setSecretAccessKey(configuration.get('amazon_secret_key'))
setAssociateTag(configuration.get('amazon_associate_tag'))


#titles=Title.select(AND(RLIKE(Title.q.isbn, "^[0-9]{13}$"), Title.q.kindID==1))

#for t in titles:
#    updateItem(updateTitle=True, updateImage=True, updateAuthors=True)








def updateItem(t, updateTitle=False, updateImage=False, updateAuthors=False, updateCategories=False):
    try:
        amazonIter=ItemLookup(t.origIsbn, IdType='ISBN', SearchIndex="Books", ResponseGroup="ItemAttributes,Images")
        amazon_authors = set()

        len_largest = 0
        for book in amazonIter:
            if len_largest < len(dir(book)):
                len_largest = len(dir(book))
                amazon_info = book 
        print amazon_info
        if updateTitle:
                    if hasattr(amazon_info,'Title'):
                        t.booktitle = amazon_info.Title

                    if hasattr(amazon_info,'Manufacturer'):
                        t.publisher = amazon_info.Manufacturer

                    if hasattr(amazon_info, "Binding"):
                        Format=amazon_info.Binding
                 
                    if amazon_info.ProductGroup=='Book':
                        t.kind_id = 1 
                    elif amazon_info.ProductGroup=='Music':
                        t.kind_id = 3
                    elif amazon_info.ProductGroup in ('DVD', 'Video'):
                        t.kidn_id = 4
                
        if updateImage:
                if t.images:
                    if not t.images.largeUrl:
                        t.images.largeUrl = amazon_info.LargeImage.URL
                    if not t.images.medUrl:
                        t.images.medUrl = amazon_info.MediumImage.URL
                    if not t.images.smallUrl:
                        t.images.smallUrl = amazon_info.SmallImage.URL
        else:
            Images(titleID=t.id, largeUrl = amazon_info.LargeImage.URL, medUrl = amazon_info.MediumImage.URL, smallUrl = amazon_info.SmallImage.URL)
   
        if updateAuthors: 
            for x in ['Author','Creator', 'Artist', 'Director']:
                if hasattr(amazon_info,x):
                    if type(getattr(amazon_info,x))==type([]):
                        amazon_authors.update(getattr(amazon_info,x))
                    else:
                        amazon_authors.add(getattr(amazon_info,x))
            
            try:
                isk_authors = {x.authorName for x in t.author}
            except:
                isk_authors = set()
            print amazon_authors, isk_authors

            #items that are in isk bout not in amazon info
            authors_to_remove = isk_authors - amazon_authors
            print authors_to_remove
            for auth in authors_to_remove:
                auth_rec = [x for x in t.author if x.authorName==auth][0]
                t.removeAuthor(auth_rec)
            
            authors_to_add = amazon_authors - isk_authors
            print authors_to_add
            for auth in authors_to_add:
                theAuthors = Author.selectBy(authorName=auth)
                theAuthorsList = list(theAuthors)

                if len(theAuthorsList) == 1:
                    t.addAuthor(theAuthorsList[0])
                elif len(theAuthorsList) == 0:
                    a = Author(authorName=auth)
                    t.addAuthor(a)
    except Exception as excep:
            print excep
            traceback.print_exc()
            pass

