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
__CHEETAH_genTime__ = 1316642132.003673
__CHEETAH_genTimestamp__ = 'Wed Sep 21 17:55:32 2011'
__CHEETAH_src__ = 'TitleEditTemplate.tmpl'
__CHEETAH_srcLastModified__ = 'Mon Jul 25 15:44:35 2011'
__CHEETAH_docstring__ = 'Autogenerated by Cheetah: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class TitleEditTemplate(Skeleton):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        super(TitleEditTemplate, self).__init__(*args, **KWs)
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
        
        write(u'''Editing ''')
        _v = VFFSL(SL,"title.booktitle",True) # u'${title.booktitle}' on line 5, col 9
        if _v is not None: write(_filter(_v, rawExpr=u'${title.booktitle}')) # from line 5, col 9.
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
        
        write(u'''<h1>Edit a Title</h1>

<form method="get" action="/titleedit">
''')
        _v = VFFSL(SL,"title.object_to_form",True) # u'$title.object_to_form' on line 12, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$title.object_to_form')) # from line 12, col 1.
        write(u'''
</form>
<h2>Author(s):</h2>
<!-- 11/10/2008 john fixed manually -->
''')
        for a in VFFSL(SL,"title.author",True): # generated from line 16, col 1
            write(u'''<div><span>''')
            _v = VFFSL(SL,"a.authorName",True) # u'$a.authorName' on line 17, col 12
            if _v is not None: write(_filter(_v, rawExpr=u'$a.authorName')) # from line 17, col 12.
            write(u'''</span><a class="listinglink" href="/authoredit?id=''')
            _v = VFFSL(SL,"a.id",True) # u'$a.id' on line 17, col 76
            if _v is not None: write(_filter(_v, rawExpr=u'$a.id')) # from line 17, col 76.
            write(u'''">edit</a></div>
''')
        write(u'''

<h2>Copies</h2>
<form action="/addtocart">
''')
        for b in VFFSL(SL,"title.books",True): # generated from line 23, col 1
            write(u'''<div class="listinggroup">
<table>
<tr>
<td>
<a class="listinglink" href="/bookedit?id=''')
            _v = VFFSL(SL,"b.id",True) # u'$b.id' on line 28, col 43
            if _v is not None: write(_filter(_v, rawExpr=u'$b.id')) # from line 28, col 43.
            write(u'''">edit</a>
</td>
<td>
<b>copy from ''')
            _v = VFFSL(SL,"b.distributor",True) # u'$b.distributor' on line 31, col 14
            if _v is not None: write(_filter(_v, rawExpr=u'$b.distributor')) # from line 31, col 14.
            write(u''' owned by ''')
            _v = VFFSL(SL,"b.owner",True) # u'$b.owner' on line 31, col 38
            if _v is not None: write(_filter(_v, rawExpr=u'$b.owner')) # from line 31, col 38.
            write(u''' <br />inventoried on ''')
            _v = VFFSL(SL,"b.inventoried_when",True) # u'$b.inventoried_when' on line 31, col 68
            if _v is not None: write(_filter(_v, rawExpr=u'$b.inventoried_when')) # from line 31, col 68.
            write(u''' at $''')
            _v = VFFSL(SL,"b.ourprice",True) # u'$b.ourprice' on line 31, col 93
            if _v is not None: write(_filter(_v, rawExpr=u'$b.ourprice')) # from line 31, col 93.
            write(u"""<br /> with status '""")
            _v = VFFSL(SL,"b.status",True) # u'$b.status' on line 31, col 124
            if _v is not None: write(_filter(_v, rawExpr=u'$b.status')) # from line 31, col 124.
            write(u"""'<br/>in location '""")
            _v = VFFSL(SL,"b.location.locationName",True) # u'$b.location.locationName' on line 31, col 152
            if _v is not None: write(_filter(_v, rawExpr=u'$b.location.locationName')) # from line 31, col 152.
            write(u'''\'<br /></b>
</td>
<td>
add this copy to cart: <input type="checkbox" name="copy_id" value="''')
            _v = VFFSL(SL,"b.id",True) # u'$b.id' on line 34, col 69
            if _v is not None: write(_filter(_v, rawExpr=u'$b.id')) # from line 34, col 69.
            write(u'''" />
[add <input style="width:80px;"type="text" length="3" name="select_x_like_''')
            _v = VFFSL(SL,"b.id",True) # u'$b.id' on line 35, col 75
            if _v is not None: write(_filter(_v, rawExpr=u'$b.id')) # from line 35, col 75.
            write(u'''" value="" /> copies like this to cart]
</td>
</tr>
</table>
</div>
''')
        write(u'''<input class="submit" type="submit" name="addtocart" value="Collect selected copies" /> <br /> <!--<br />
<input class="submit" type="submit" name="delete" onclick="return confirm(\'Are you sure?\');" value="Delete selected copies" />-->
</form>

<h2>Keywords::</h2>
''')
        for c in VFFSL(SL,"title.categorys",True): # generated from line 46, col 1
            write(u'''<div class="listing"><span class="listing">''')
            _v = VFFSL(SL,"c.categoryName",True) # u'$c.categoryName' on line 47, col 44
            if _v is not None: write(_filter(_v, rawExpr=u'$c.categoryName')) # from line 47, col 44.
            write(u'''</span><a class="listinglink" href="/categoryedit?id=''')
            _v = VFFSL(SL,"c.id",True) # u'$c.id' on line 47, col 112
            if _v is not None: write(_filter(_v, rawExpr=u'$c.id')) # from line 47, col 112.
            write(u'''">edit</a></div>
''')
        write(u'''


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

    _mainCheetahMethod_for_TitleEditTemplate= 'writeBody'

## END CLASS DEFINITION

if not hasattr(TitleEditTemplate, '_initCheetahAttributes'):
    templateAPIClass = getattr(TitleEditTemplate, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(TitleEditTemplate)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=TitleEditTemplate()).run()


