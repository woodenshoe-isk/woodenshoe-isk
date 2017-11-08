#!/usr/bin/env python
# -*- coding: UTF-8 -*-




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
from Cheetah.compat import unicode
from .SkeletonBase import SkeletonBase

##################################################
## MODULE CONSTANTS
VFFSL=valueFromFrameOrSearchList
VFSL=valueFromSearchList
VFN=valueForName
currentTime=time.time
__CHEETAH_version__ = '3.0.0'
__CHEETAH_versionTuple__ = (3, 0, 0, 'final', 1)
__CHEETAH_genTime__ = 1510105566.1029532
__CHEETAH_genTimestamp__ = 'Wed Nov  8 01:46:06 2017'
__CHEETAH_src__ = 'Skeleton.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Nov  8 00:51:24 2017'
__CHEETAH_docstring__ = 'Autogenerated by Cheetah: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class Skeleton(SkeletonBase):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        super(Skeleton, self).__init__(*args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = 'searchList namespaces filter filtersLib errorCatcher'.split()
            for k,v in KWs.items():
                if k in allowedKWs: cheetahKWArgs[k] = v
            self._initCheetahInstance(**cheetahKWArgs)
        

    def headscripts(self, **KWS):



        ## CHEETAH: generated from #block headscripts at line 30, col 1.
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
        
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def head(self, **KWS):



        ## CHEETAH: generated from #block head at line 11, col 1.
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
        
        # <script src="/javascript/sorttable.js"></script>
        write('''<script src="/javascript/functions.js"></script>

<!--This adds jquery & jquery-ui -->

<script type=\'text/javascript\' src=\'/javascript/jquery-1.12.3.min.js\'></script>

<link type="text/css" href="/javascript/jquery-ui-1.12.0-rc.2.custom/jquery-ui.min.css" rel="Stylesheet" />
<script type=\'text/javascript\' src=\'/javascript/jquery-ui-1.12.0-rc.2.custom/jquery-ui.min.js\'></script>

<link type="text/css" href="/javascript/datatables.min.css" rel="Stylesheet" />\t
<script type=\'text/javascript\' src=\'/javascript/datatables.min.js\'></script>
''')
        # <script type='text/javascript' src='/javascript/FixedHeader.js'></script>
        write('''<script type=\'text/javascript\' src=\'/javascript/client-side-logger.js\'></script>

<link href="/style/main.css" type="text/css" rel="stylesheet"/>

''')
        # head scripts should go here.
        self.headscripts(trans=trans)
        write('''
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def generateMenu(self, iterable, **KWS):



        ## CHEETAH: generated from #def generateMenu( $iterable ) at line 40, col 1.
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
        
        for i in VFFSL(SL,"iterable",True): # generated from line 41, col 1
            write("""    <li><a href='""")
            _v = VFFSL(SL,"i",True)[1] # '$i[1]' on line 42, col 18
            if _v is not None: write(_filter(_v, rawExpr='$i[1]')) # from line 42, col 18.
            write("""'>""")
            _v = VFFSL(SL,"i",True)[0] # '$i[0]' on line 42, col 25
            if _v is not None: write(_filter(_v, rawExpr='$i[0]')) # from line 42, col 25.
            write('''</a>
''')
            if VFFSL(SL,"i",True)[2]: # generated from line 43, col 5
                write('''    <ul>
    ''')
                _v = VFFSL(SL,"generateMenu",False)( VFFSL(SL,"i",True)[2] ) # '$generateMenu( $i[2] )' on line 45, col 5
                if _v is not None: write(_filter(_v, rawExpr='$generateMenu( $i[2] )')) # from line 45, col 5.
                write('''
    </ul>
''')
            write('''    </li>
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def body(self, **KWS):



        ## CHEETAH: generated from #block body at line 64, col 1.
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
        
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def respond(self, trans=None):



        ## CHEETAH: main method generated for this template
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
        
        # framework for other templates
        write('''
<head>
<title>''')
        _v = VFFSL(SL,"pagetitle",True) # '$pagetitle' on line 8, col 8
        if _v is not None: write(_filter(_v, rawExpr='$pagetitle')) # from line 8, col 8.
        write('''</title>
<meta HTTP-EQUIV="Pragma" content="no-cache">
<meta HTTP-EQUIV="Expires" content="-1">
''')
        self.head(trans=trans)
        write('''</head>
<body>

''')
        # define generate menu function. Requires an iterable
        # of triplets: [('MenuName', 'MenuURL', [ submenu of the same format if submenu ]), ]
        # can recursively do submenus
        write('''
<div class="toolbar">
<ul class="nav">
''')
        # actually generate the menus using menudata.
        # Class works as outlined above in generateMenu function def
        _v = VFFSL(SL,"generateMenu",False)( VFN(VFFSL(SL,"menudata",True),"getMenuData",False)() ) # '$generateMenu( $menudata.getMenuData() )' on line 56, col 1
        if _v is not None: write(_filter(_v, rawExpr='$generateMenu( $menudata.getMenuData() )')) # from line 56, col 1.
        write('''
</ul>
</div>
''')
        lastsearch = 0
        if VFFSL(SL,"lastsearch",True): # generated from line 60, col 1
            write('''<a href="''')
            _v = VFFSL(SL,"lastsearch",True) # '$lastsearch' on line 61, col 10
            if _v is not None: write(_filter(_v, rawExpr='$lastsearch')) # from line 61, col 10.
            write('''">Return to search results...</a>
''')
        write('''<div class="main">
''')
        self.body(trans=trans)
        write('''</div>
</body>
</html>
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

    _mainCheetahMethod_for_Skeleton= 'respond'

## END CLASS DEFINITION

if not hasattr(Skeleton, '_initCheetahAttributes'):
    templateAPIClass = getattr(Skeleton, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(Skeleton)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://cheetahtemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=Skeleton()).run()

