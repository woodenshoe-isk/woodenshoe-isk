import sys
import os
import urllib2

from sqlobject import *
from components import db
from config import configuration
from SQLObjectWithFormGlue import SQLObjectWithFormGlue
from mx.DateTime import now



class Images(SQLObjectWithFormGlue):
    _connection = db.conn()
    _cfg = configuration()
    
    title = ForeignKey('Title') 
    createdAt = DateCol(default=now)
    updatedAt = DateCol(default=now)
    
    class sqlmeta:
        fromDatabase = True
        
    def retrieve_image(self, size='small'):
         isbn = self.title.origIsbn
         image_dir = image_directory_root = self._cfg.get('image_directory_root')
         default_image = self._cfg('image_default_small')

         for dirname in [isbn[i:i+3] for i in range(3, 12, 3)]:
             image_dir = os.path.join(image_dir, dirname)
 
         image_filename = os.path.join(image_dir, isbn + '_' + size + '.jpg')
         if os.path.exists(image_filename):
            with open(image_filename, 'rb') as image_file:
                imagedata = image_file.read()
            return imagedata
         else:
            try:
                url = getattr(self.title.images, '%sUrl'%size)
                imagedata = urllib2.urlopen(url).read()
 
            except Exception as e1:
                print>>sys.stderr, e1
                with open(default_image, 'rb') as image_file:
                    imagedata = image_file.read()
                    return imagedata
 
            else:
                try:
                   if not os.path.exists(image_dir):
                       image_dir = image_directory_root
                       for dirname in [isbn[i:i+3] for i in range(3, 12, 3)]:
                           image_dir = os.path.join(image_dir, dirname)
                           os.path.mkdir(image_dir)
 
                   with open(image_filename, 'wb') as image_file:
                       image_file.write(imagedata)
                except Exception as e2:
                    print>>sys.stderr, e2
                    with open(default_image, 'rb') as image_file:
                        imagedata = image_file.read()
                        return imagedata
                else:
                    return imagedata

    def retrieve_image_url(self, size='small'):
         isbn = self.title.origIsbn
         image_dir = image_directory_root = self._cfg.get('image_directory_root')

         for dirname in [isbn[i:i+3] for i in range(3, 12, 3)]:
             image_dir = os.path.join(image_dir, dirname)
 
         image_filename = os.path.join(image_dir, isbn + '_' + size + '.jpg')
         if os.path.exists(image_filename):
            relative_image_url = os.path.relpath(image_filename, image_directory_root)
            return os.path.join('/images/', relative_image_url)
         else:
            try:
                url = getattr(self.title.images, '%sUrl'%size)
                imagedata = urllib2.urlopen(url).read()
 
            except Exception as e1:
                print>>sys.stderr, e1
                relative_image_url = os.path.relpath(default_image, image_directory_root)
                return os.path.join('/images/', relative_image_url)
 
            else:
                try:
                   if not os.path.exists(image_dir):
                       image_dir = image_directory_root
                       for dirname in [isbn[i:i+3] for i in range(3, 12, 3)]:
                           image_dir = os.path.join(image_dir, dirname)
                           os.path.mkdir(image_dir)
 
                   with open(image_filename, 'wb') as image_file:
                       image_file.write(imagedata)
                except Exception as e2:
                    print>>sys.stderr, e2
                    relative_image_url = os.path.relpath(default_image, image_directory_root)
                    return os.path.join('/images/', relative_image_url)
                else:
                    relative_image_url = os.path.relpath(image_filename, image_directory_root)
                    return os.path.join('/images/', relative_image_url)
