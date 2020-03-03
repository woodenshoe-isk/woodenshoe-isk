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
from objects.author import Author

##################################################
## MODULE CONSTANTS
VFFSL = valueFromFrameOrSearchList
VFSL = valueFromSearchList
VFN = valueForName
currentTime = time.time
__CHEETAH_version__ = "3.0.0"
__CHEETAH_versionTuple__ = (3, 0, 0, "final", 1)
__CHEETAH_genTime__ = 1510105565.9839058
__CHEETAH_genTimestamp__ = "Wed Nov  8 01:46:05 2017"
__CHEETAH_src__ = "EditTemplate.tmpl"
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


class EditTemplate(Skeleton):

    ##################################################
    ## CHEETAH GENERATED METHODS

    def __init__(self, *args, **KWs):

        super(EditTemplate, self).__init__(*args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = "searchList namespaces filter filtersLib errorCatcher".split()
            for k, v in KWs.items():
                if k in allowedKWs:
                    cheetahKWArgs[k] = v
            self._initCheetahInstance(**cheetahKWArgs)

    def headscripts(self, **KWS):

        ## CHEETAH: generated from #def headscripts at line 9, col 1.
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
            """<script type="text/javascript">
    jQuery(document).ready(function() {
        jQuery( ".editform" ).submit(function( event ) {
            if ( confirm("Do you really want to change this record?")) {
                return true;
            } else {
                event.preventDefault();     
                jQuery(this).trigger(\'reset\');
            };
        });
    });
</script>
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

        # Edit record information
        # Parent class to be subclassed
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

    _mainCheetahMethod_for_EditTemplate = "writeBody"


## END CLASS DEFINITION

if not hasattr(EditTemplate, "_initCheetahAttributes"):
    templateAPIClass = getattr(EditTemplate, "_CHEETAH_templateClass", Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(EditTemplate)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://cheetahtemplate.org/

##################################################
## if run from command line:
if __name__ == "__main__":
    from Cheetah.TemplateCmdLineIface import CmdLineIface

    CmdLineIface(templateObj=EditTemplate()).run()
