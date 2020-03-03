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
from Cheetah.NameMapper import (
    NotFound,
    valueForName,
    valueFromSearchList,
    valueFromFrameOrSearchList,
)
from Cheetah.CacheRegion import CacheRegion
import Cheetah.Filters as Filters
import Cheetah.ErrorCatchers as ErrorCatchers
from Cheetah.compat import unicode
from inventoryserver.Skeleton import Skeleton

##################################################
## MODULE CONSTANTS
VFFSL = valueFromFrameOrSearchList
VFSL = valueFromSearchList
VFN = valueForName
currentTime = time.time
__CHEETAH_version__ = "3.0.0"
__CHEETAH_versionTuple__ = (3, 0, 0, "final", 1)
__CHEETAH_genTime__ = 1510105566.010908
__CHEETAH_genTimestamp__ = "Wed Nov  8 01:46:06 2017"
__CHEETAH_src__ = "LocationListTemplate.tmpl"
__CHEETAH_srcLastModified__ = "Wed Nov  8 00:51:24 2017"
__CHEETAH_docstring__ = "Autogenerated by Cheetah: The Python-Powered Template Engine"

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
        "This template was compiled with Cheetah version"
        " %s. Templates compiled before version %s must be recompiled."
        % (__CHEETAH_version__, RequiredCheetahVersion)
    )

##################################################
## CLASSES


class LocationListTemplate(Skeleton):

    ##################################################
    ## CHEETAH GENERATED METHODS

    def __init__(self, *args, **KWs):

        super(LocationListTemplate, self).__init__(*args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = "searchList namespaces filter filtersLib errorCatcher".split()
            for k, v in KWs.items():
                if k in allowedKWs:
                    cheetahKWArgs[k] = v
            self._initCheetahInstance(**cheetahKWArgs)

    def pagetitle(self, **KWS):

        ## CHEETAH: generated from #def pagetitle at line 7, col 1.
        trans = KWS.get("trans")
        if (
            not trans
            and not self._CHEETAH__isBuffering
            and not callable(self.transaction)
        ):
            trans = self.transaction  # is None unless self.awake() was called
        if not trans:
            trans = DummyTransaction()
            _dummyTrans = True
        else:
            _dummyTrans = False
        write = trans.response().write
        SL = self._CHEETAH__searchList
        _filter = self._CHEETAH__currentFilter

        ########################################
        ## START - generated method body

        write(
            """Locations
"""
        )

        ########################################
        ## END - generated method body

        return _dummyTrans and trans.response().getvalue() or ""

    def body(self, **KWS):

        ## CHEETAH: generated from #def body at line 11, col 1.
        trans = KWS.get("trans")
        if (
            not trans
            and not self._CHEETAH__isBuffering
            and not callable(self.transaction)
        ):
            trans = self.transaction  # is None unless self.awake() was called
        if not trans:
            trans = DummyTransaction()
            _dummyTrans = True
        else:
            _dummyTrans = False
        write = trans.response().write
        SL = self._CHEETAH__searchList
        _filter = self._CHEETAH__currentFilter

        ########################################
        ## START - generated method body

        write(
            """<h1>Locations</h1>
<ul>
"""
        )
        for l in VFFSL(SL, "locations", True):  # generated from line 14, col 1
            write("""<li><a href="/admin/locationedit?id=""")
            _v = VFFSL(SL, "l.id", True)  # '$l.id' on line 15, col 37
            if _v is not None:
                write(_filter(_v, rawExpr="$l.id"))  # from line 15, col 37.
            write("""">""")
            _v = VFFSL(
                SL, "l.locationName", True
            )  # '$l.locationName' on line 15, col 44
            if _v is not None:
                write(_filter(_v, rawExpr="$l.locationName"))  # from line 15, col 44.
            write(
                """</></li>
"""
            )
        write(
            """</ul>
<a href="/admin/locationedit">Add a new location</a>
"""
        )

        ########################################
        ## END - generated method body

        return _dummyTrans and trans.response().getvalue() or ""

    def writeBody(self, **KWS):

        ## CHEETAH: main method generated for this template
        trans = KWS.get("trans")
        if (
            not trans
            and not self._CHEETAH__isBuffering
            and not callable(self.transaction)
        ):
            trans = self.transaction  # is None unless self.awake() was called
        if not trans:
            trans = DummyTransaction()
            _dummyTrans = True
        else:
            _dummyTrans = False
        write = trans.response().write
        SL = self._CHEETAH__searchList
        _filter = self._CHEETAH__currentFilter

        ########################################
        ## START - generated method body

        # List all locations. Each location is linkded
        # to a location edit page for it to be edited
        write(
            """


"""
        )

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

    _mainCheetahMethod_for_LocationListTemplate = "writeBody"


## END CLASS DEFINITION

if not hasattr(LocationListTemplate, "_initCheetahAttributes"):
    templateAPIClass = getattr(LocationListTemplate, "_CHEETAH_templateClass", Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(LocationListTemplate)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://cheetahtemplate.org/

##################################################
## if run from command line:
if __name__ == "__main__":
    from Cheetah.TemplateCmdLineIface import CmdLineIface

    CmdLineIface(templateObj=LocationListTemplate()).run()
