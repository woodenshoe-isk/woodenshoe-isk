#!/usr/bin/env python




##################################################
## DEPENDENCIES
import sys
import os
import os.path
try:
    import builtins as builtin
except ImportError:
    import __builtin__ as builtin
from os.path import getmtime, exists
import time
import types
from Cheetah.Version import MinCompatibleVersion as RequiredCheetahVersion
from Cheetah.Version import MinCompatibleVersionTuple as RequiredCheetahVersionTuple
from Cheetah.Template import Template
from Cheetah.DummyTransaction import *
from Cheetah.NameMapper import NotFound, valueForName, valueFromSearchList, valueFromFrameOrSearchList
from Cheetah.CacheRegion import CacheRegion
import Cheetah.Filters as Filters
import Cheetah.ErrorCatchers as ErrorCatchers
from Skeleton import Skeleton

##################################################
## MODULE CONSTANTS
VFFSL=valueFromFrameOrSearchList
VFSL=valueFromSearchList
VFN=valueForName
currentTime=time.time
__CHEETAH_version__ = '2.4.3'
__CHEETAH_versionTuple__ = (2, 4, 3, 'development', 0)
__CHEETAH_genTime__ = 1316642131.993604
__CHEETAH_genTimestamp__ = 'Wed Sep 21 17:55:31 2011'
__CHEETAH_src__ = 'AuthorEditTemplate.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Jun  8 16:13:20 2011'
__CHEETAH_docstring__ = 'Autogenerated by Cheetah: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class AuthorEditTemplate(Skeleton):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        super(AuthorEditTemplate, self).__init__(*args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = 'searchList namespaces filter filtersLib errorCatcher'.split()
            for k,v in KWs.items():
                if k in allowedKWs: cheetahKWArgs[k] = v
            self._initCheetahInstance(**cheetahKWArgs)
        

    def pagetitle(self, **KWS):



        ## CHEETAH: generated from #def pagetitle at line 4, col 1.
        trans = KWS.get("trans")
        if (not trans and not self._CHEETAH__isBuffering and not callable(self.transaction)):
            trans = self.transaction # is None unless self.awake() was called
        if not trans:
            trans = DummyTransaction()
            _dummyTrans = True
        else: _dummyTrans = False
        write = trans.response().write
        SL = self._CHEETAH__searchList
        _filter = self._CHEETAH__currentFilter
        
        ########################################
        ## START - generated method body
        
        write(u'''Editing author ''')
        _v = VFFSL(SL,"author.authorName",True) # u'$author.authorName' on line 5, col 16
        if _v is not None: write(_filter(_v, rawExpr=u'$author.authorName')) # from line 5, col 16.
        write(u'''
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def body(self, **KWS):



        ## CHEETAH: generated from #def body at line 8, col 1.
        trans = KWS.get("trans")
        if (not trans and not self._CHEETAH__isBuffering and not callable(self.transaction)):
            trans = self.transaction # is None unless self.awake() was called
        if not trans:
            trans = DummyTransaction()
            _dummyTrans = True
        else: _dummyTrans = False
        write = trans.response().write
        SL = self._CHEETAH__searchList
        _filter = self._CHEETAH__currentFilter
        
        ########################################
        ## START - generated method body
        
        write(u'''<h1>Author record for ''')
        _v = VFFSL(SL,"author.authorName",True) # u'${author.authorName}' on line 9, col 23
        if _v is not None: write(_filter(_v, rawExpr=u'${author.authorName}')) # from line 9, col 23.
        write(u'''</h1>
<form method="get" action="/authoredit">
''')
        _v = VFFSL(SL,"author.object_to_form",True) # u'$author.object_to_form' on line 11, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$author.object_to_form')) # from line 11, col 1.
        write(u'''
</form>
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def writeBody(self, **KWS):



        ## CHEETAH: main method generated for this template
        trans = KWS.get("trans")
        if (not trans and not self._CHEETAH__isBuffering and not callable(self.transaction)):
            trans = self.transaction # is None unless self.awake() was called
        if not trans:
            trans = DummyTransaction()
            _dummyTrans = True
        else: _dummyTrans = False
        write = trans.response().write
        SL = self._CHEETAH__searchList
        _filter = self._CHEETAH__currentFilter
        
        ########################################
        ## START - generated method body
        
        write(u'''

''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        
    ##################################################
    ## CHEETAH GENERATED ATTRIBUTES


    _CHEETAH__instanceInitialized = False

    _CHEETAH_version = __CHEETAH_version__

    _CHEETAH_versionTuple = __CHEETAH_versionTuple__

    _CHEETAH_genTime = __CHEETAH_genTime__

    _CHEETAH_genTimestamp = __CHEETAH_genTimestamp__

    _CHEETAH_src = __CHEETAH_src__

    _CHEETAH_srcLastModified = __CHEETAH_srcLastModified__

    _mainCheetahMethod_for_AuthorEditTemplate= 'writeBody'

## END CLASS DEFINITION

if not hasattr(AuthorEditTemplate, '_initCheetahAttributes'):
    templateAPIClass = getattr(AuthorEditTemplate, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(AuthorEditTemplate)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=AuthorEditTemplate()).run()


