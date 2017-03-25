import sys
import os
import urllib.request, urllib.error, urllib.parse

from sqlobject import *
from tools import db
from config.config import configuration
from .SQLObjectWithFormGlue import SQLObjectWithFormGlue
from tools.now import Now



class Images(SQLObjectWithFormGlue):
    _cfg = configuration()
    
    title = ForeignKey('Title') 
    createdAt = DateCol(default=Now.now)
    updatedAt = DateCol(default=Now.now)
    
    class sqlmeta:
        fromDatabase = True
 
#     retrieve image from cache. not used in current model.    
#     def retrieve_image(self, size='small'):
#          isbn = self.title.origIsbn
#          image_dir = image_directory_root = self._cfg.get('image_directory_root')
#          default_image = self._cfg.get('image_default_small')
# 
#          for dirname in [isbn[i:i+3] for i in range(3, 12, 3)]:
#              image_dir = os.path.join(image_dir, dirname)
#  
#          image_filename = os.path.join(image_dir, isbn + '_' + size + '.jpg')
#          if os.path.exists(image_filename):
#             with open(image_filename, 'rb') as image_file:
#                 imagedata = image_file.read()
#             return imagedata
#          else:
#             try:
#                 url = getattr(self.title.images, '%sUrl'%size)
#                 imagedata = urllib2.urlopen(url).read()
#  
#             except Exception as e1:
#                 print>>sys.stderr, e1
#                 with open(default_image, 'rb') as image_file:
#                     imagedata = image_file.read()
#                     return imagedata
#  
#             else:
#                 try:
#                    if not os.path.exists(image_dir):
#                        image_dir = image_directory_root
#                        for dirname in [isbn[i:i+3] for i in range(3, 12, 3)]:
#                            image_dir = os.path.join(image_dir, dirname)
#                            os.path.mkdir(image_dir)
#  
#                    with open(image_filename, 'wb') as image_file:
#                        image_file.write(imagedata)
#                 except Exception as e2:
#                     print>>sys.stderr, e2
#                     with open(default_image, 'rb') as image_file:
#                         imagedata = image_file.read()
#                         return imagedata
#                 else:
#                     return imagedata
    
    
    #we link changes of any url to change in updated_at date
    def _set_small_url(self, value):
        self.updated_at=Now.now
        self._SO_set_small_url(value)

    def _set_med_url(self, value):
        self.updated_at=Now.now
        self._SO_set_med_url(value)

    def _set_large_url(self, value):
        self.updated_at=Now.now
        self._SO_set_large_url(value)

    
    #retrieve url for image that exists in cache
    def retrieve_image_url(self, size='small'):
         isbn = self.title.origIsbn
         image_dir = image_directory_root = self._cfg.get('image_directory_root')
         default_image = self._cfg.get('image_default_small')
         
         #we structure the chache based on the isbn
         #since they all start in 978 ir 979 we discard those
         #we also discard the check digit. So it's a 3-tiered directory structure of
         #3-digit filenames from the isbn
         for dirname in [isbn[i:i+3] for i in range(3, 12, 3)]:
             image_dir = os.path.join(image_dir, dirname)
         
         #actual filename is <isbn>_<size>.<filetype>
         remote_url = getattr(self.title.images, '%sUrl'%size)
         dummy, filetype= os.path.splitext(remote_url)
         print("filetype is ", filetype, file=sys.stderr)
         
         #if we have the image already, we get its url from our cache
         image_filename = os.path.join(image_dir, isbn + '_' + size + filetype)
         if os.path.exists(image_filename):
            relative_image_url = os.path.relpath(image_filename, image_directory_root)
            print("image file {url}".format(url=relative_image_url), file=sys.stderr)
            return os.path.join('/images/', relative_image_url)
         else:
            #if we don't have it, we try to get the image from
            #the remote url
            try:
                imagedata = urllib.request.urlopen(remote_url).read()
 
            except Exception as e1:
                #if we can't retrieve, get the default image relative url
                print(e1, file=sys.stderr)
                relative_image_url = os.path.relpath(default_image, image_directory_root)
                return os.path.join('/images/', relative_image_url)
 
            else:
                #so, if we get the image we see if the path to its cache directiory exists
                #if it doesn't we create the cache directory tree for the file "xxx/xxx/xxx"
                try:
                   if not os.path.exists(image_dir):
                       image_dir = image_directory_root
                       for dirname in [isbn[i:i+3] for i in range(3, 12, 3)]:
                           image_dir = os.path.join(image_dir, dirname)
                           if not os.path.exists(image_dir):
                               os.mkdir(image_dir)
                   #write the image data to disk
                   with open(image_filename, 'wb') as image_file:
                       image_file.write(imagedata)
                #if we have a file I/O problem we again return default image
                except Exception as e2:
                    print(e2, file=sys.stderr)
                    relative_image_url = os.path.relpath(default_image, image_directory_root)
                    return os.path.join('/images/', relative_image_url)
                else:
                    #if we succeed in retrieving and writing
                    #we return the relative path of the file
                    relative_image_url = os.path.relpath(image_filename, image_directory_root)
                    return os.path.join('/images/', relative_image_url)
