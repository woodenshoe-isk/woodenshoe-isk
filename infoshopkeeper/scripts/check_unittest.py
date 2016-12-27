import inspect

import os, sys
import imp

import inventoryserver
from inventoryserver import server

def get_classes_and_methods( package ):
    results1=[]
    for memb in inspect.getmembers(package):
        if inspect.isfunction( memb[1] ):
            if memb[1].__module__==package.__name__:
                results1.append(memb[1].__name__)
        elif inspect.isclass(memb[1]):
            if memb[1].__module__==package.__name__:
                results1.append( get_classes_and_methods( memb[1]))

    return {package.__name__:results1}   

def process_file( dirName, file):
     module_name=os.path.splitext(file)[0]
     modules={}
     try:
         if not dirName in sys.path:
              sys.path.append(dirName)
         module1 = imp.load_source(module_name, os.path.join(dirName, file)) 
     except Exception as e:
        # print e
         pass  #rint module_name
     else:
        modules[module_name]= get_classes_and_methods(module1)
        print(("     " + module_name)) 
        for module2 in modules:
             print(('          ', modules[module2]))

base_dir=os.getcwd()
for dirName, subdirList, fileList in os.walk(base_dir):
     print(dirName)
     test_files=[]
     non_test_files=[]
     for file in fileList:
         if file.endswith('.py') and os.path.join(dirName, file)!=os.path.abspath(__file__):
             if file.startswith('test'):
                 test_files.append(file)
             else:
                 non_test_files.append(file)
             
     for file in test_files:        
          process_file(dirName, file)
     for file in non_test_files:
          process_file(dirName, file)
print((get_classes_and_methods(inventoryserver.server)))
