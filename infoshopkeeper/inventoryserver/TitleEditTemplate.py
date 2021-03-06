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
import urllib
from .EditTemplate import EditTemplate

##################################################
## MODULE CONSTANTS
VFFSL = valueFromFrameOrSearchList
VFSL = valueFromSearchList
VFN = valueForName
currentTime = time.time
__CHEETAH_version__ = "3.0.0"
__CHEETAH_versionTuple__ = (3, 0, 0, "final", 1)
__CHEETAH_genTime__ = 1510105566.2040875
__CHEETAH_genTimestamp__ = "Wed Nov  8 01:46:06 2017"
__CHEETAH_src__ = "TitleEditTemplate.tmpl"
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


class TitleEditTemplate(EditTemplate):

    ##################################################
    ## CHEETAH GENERATED METHODS

    def __init__(self, *args, **KWs):

        super(TitleEditTemplate, self).__init__(*args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = "searchList namespaces filter filtersLib errorCatcher".split()
            for k, v in KWs.items():
                if k in allowedKWs:
                    cheetahKWArgs[k] = v
            self._initCheetahInstance(**cheetahKWArgs)

    def headscripts(self, **KWS):

        ## CHEETAH: generated from #def headscripts at line 10, col 1.
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

        _v = VFN(VFFSL(SL, "EditTemplate", True), "headscripts", False)(
            VFFSL(SL, "self", True)
        )  # '$EditTemplate.headscripts($self)' on line 11, col 1
        if _v is not None:
            write(
                _filter(_v, rawExpr="$EditTemplate.headscripts($self)")
            )  # from line 11, col 1.
        write(
            """
<script type="text/javascript">                                         
    jQuery(document).ready(function() {
//         //Ajax setup for error handling
//         jQuery.ajaxSetup({"error":function(XMLHttpRequest,textStatus, errorThrown) {   
//                 alert(textStatus);
//                 alert(errorThrown);
//                 alert(XMLHttpRequest.responseText);          
//         }});

        //enable autocomplete for title
        jQuery(\'#id_booktitle\').autocomplete({
            source: \'title_autocomplete\',
        });   
        
        jQuery(\'.print_link\').bind(\'click\', function() {
            jQuery.get(jQuery(this)[0].href);
            return false;
        });
    });
</script>
"""
        )

        ########################################
        ## END - generated method body

        return _dummyTrans and trans.response().getvalue() or ""

    def pagetitle(self, **KWS):

        ## CHEETAH: generated from #def pagetitle at line 34, col 1.
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

        write("""Editing """)
        _v = VFFSL(
            SL, "title.booktitle", True
        )  # '${title.booktitle}' on line 35, col 9
        if _v is not None:
            write(_filter(_v, rawExpr="${title.booktitle}"))  # from line 35, col 9.
        write(
            """
"""
        )

        ########################################
        ## END - generated method body

        return _dummyTrans and trans.response().getvalue() or ""

    def body(self, **KWS):

        ## CHEETAH: generated from #def body at line 38, col 1.
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
            """<h1>Edit the Information for a Title</h1>

"""
        )
        # if configured to show image we show an image of the title
        if VFFSL(SL, "should_show_images", True):  # generated from line 42, col 1
            if VFFSL(SL, "title.images", True):  # generated from line 43, col 1
                write('''<div id="main_image"><img src="''')
                _v = VFN(VFFSL(SL, "title.images", True), "retrieve_image_url", False)(
                    "large"
                )  # "$title.images.retrieve_image_url('large')" on line 44, col 32
                if _v is not None:
                    write(
                        _filter(_v, rawExpr="$title.images.retrieve_image_url('large')")
                    )  # from line 44, col 32.
                write(
                    """"><br></div>
"""
                )
        write(
            """

"""
        )
        # show the title info as editable form
        write(
            """<form class=\'editform\' method="get" action="/titleedit">
"""
        )
        _v = VFFSL(
            SL, "title.object_to_form", True
        )  # '$title.object_to_form' on line 51, col 1
        if _v is not None:
            write(_filter(_v, rawExpr="$title.object_to_form"))  # from line 51, col 1.
        write(
            """
</form>

"""
        )
        # show the author records with button to edit each author record
        write(
            """<h2>Author(s):</h2>
<!-- 11/10/2008 john fixed manually -->
"""
        )
        for a in VFFSL(SL, "title.author", True):  # generated from line 57, col 1
            write("""<div><span>""")
            _v = VFFSL(SL, "a.authorName", True)  # '$a.authorName' on line 58, col 12
            if _v is not None:
                write(_filter(_v, rawExpr="$a.authorName"))  # from line 58, col 12.
            write("""</span><a class="listinglink" href="/authoredit?id=""")
            _v = VFFSL(SL, "a.id", True)  # '$a.id' on line 58, col 76
            if _v is not None:
                write(_filter(_v, rawExpr="$a.id"))  # from line 58, col 76.
            write("""&title_id=""")
            _v = VFFSL(SL, "title.id", True)  # '$title.id' on line 58, col 91
            if _v is not None:
                write(_filter(_v, rawExpr="$title.id"))  # from line 58, col 91.
            write(
                """&new_author=False">edit</a><a class="listinglink" href="/titleedit?id="""
            )
            _v = VFFSL(SL, "title.id", True)  # '$title.id' on line 58, col 170
            if _v is not None:
                write(_filter(_v, rawExpr="$title.id"))  # from line 58, col 170.
            write("""&author_id=""")
            _v = VFFSL(SL, "a.id", True)  # '$a.id' on line 58, col 190
            if _v is not None:
                write(_filter(_v, rawExpr="$a.id"))  # from line 58, col 190.
            write(
                """&remove_author=True&new_author=False">remove</a></div>
"""
            )
        write("""<div><a class="listinglink" href="/authoredit?title_id=""")
        _v = VFFSL(SL, "title.id", True)  # '$title.id' on line 60, col 56
        if _v is not None:
            write(_filter(_v, rawExpr="$title.id"))  # from line 60, col 56.
        write(
            """&new_author=True">Add Author</a><div>

"""
        )
        # show records for each individual copy.
        # each is editable in a book edit template
        write(
            """<h2>Copies</h2>
<form action="/addtocart">
"""
        )
        for b in VFFSL(SL, "title.books", True):  # generated from line 66, col 1
            write(
                """<div class="listinggroup">
<table>
<tr>
<td>
<ul style=\'list-style-type:none;\'>
<li><a class="listinglink" href="/bookedit?id="""
            )
            _v = VFFSL(SL, "b.id", True)  # '$b.id' on line 72, col 47
            if _v is not None:
                write(_filter(_v, rawExpr="$b.id"))  # from line 72, col 47.
            write(
                """">edit</a></li>
<li><a class="listinglink print_link" href=\'/admin/print_label?booktitle=urllib.quote_plus("""
            )
            _v = VFFSL(
                SL, "b.title.booktitle", True
            )  # '$b.title.booktitle' on line 73, col 92
            if _v is not None:
                write(
                    _filter(_v, rawExpr="$b.title.booktitle")
                )  # from line 73, col 92.
            write(""")&isbn=""")
            _v = VFFSL(SL, "b.title.isbn", True)  # '$b.title.isbn' on line 73, col 117
            if _v is not None:
                write(_filter(_v, rawExpr="$b.title.isbn"))  # from line 73, col 117.
            write("""&authorstring=urllib.quote_plus(""")
            _v = VFFSL(
                SL, "b.title.authors_as_string", True
            )  # '$b.title.authors_as_string' on line 73, col 162
            if _v is not None:
                write(
                    _filter(_v, rawExpr="$b.title.authors_as_string")
                )  # from line 73, col 162.
            write(""")&ourprice=""")
            _v = VFFSL(SL, "b.ourprice", True)  # '$b.ourprice' on line 73, col 199
            if _v is not None:
                write(_filter(_v, rawExpr="$b.ourprice"))  # from line 73, col 199.
            write("""&listprice=""")
            _v = VFFSL(SL, "b.listprice", True)  # '$b.listprice' on line 73, col 221
            if _v is not None:
                write(_filter(_v, rawExpr="$b.listprice"))  # from line 73, col 221.
            write(
                """'>Print label</li>
</ul>
</td>
<td>
<b>copy from """
            )
            _v = VFFSL(SL, "b.distributor", True)  # '$b.distributor' on line 77, col 14
            if _v is not None:
                write(_filter(_v, rawExpr="$b.distributor"))  # from line 77, col 14.
            write(""" owned by """)
            _v = VFFSL(SL, "b.owner", True)  # '$b.owner' on line 77, col 38
            if _v is not None:
                write(_filter(_v, rawExpr="$b.owner"))  # from line 77, col 38.
            write(
                """ <br />
inventoried on """
            )
            _v = VFFSL(
                SL, "b.inventoried_when", True
            )  # '$b.inventoried_when' on line 78, col 16
            if _v is not None:
                write(
                    _filter(_v, rawExpr="$b.inventoried_when")
                )  # from line 78, col 16.
            write(""" at $""")
            _v = VFFSL(SL, "b.ourprice", True)  # '$b.ourprice' on line 78, col 41
            if _v is not None:
                write(_filter(_v, rawExpr="$b.ourprice"))  # from line 78, col 41.
            write(
                """<br />
with status '"""
            )
            _v = VFFSL(SL, "b.status", True)  # '$b.status' on line 79, col 14
            if _v is not None:
                write(_filter(_v, rawExpr="$b.status"))  # from line 79, col 14.
            write(
                """'
"""
            )
            if VFFSL(SL, "b.status", True) != "STOCK":  # generated from line 80, col 1
                write(""" on """)
                _v = VFFSL(SL, "b.sold_when", True)  # '$b.sold_when' on line 81, col 5
                if _v is not None:
                    write(_filter(_v, rawExpr="$b.sold_when"))  # from line 81, col 5.
                write(
                    """
"""
                )
            write(
                """<br/>
in location '"""
            )
            _v = VFFSL(
                SL, "b.location.locationName", True
            )  # '$b.location.locationName' on line 84, col 14
            if _v is not None:
                write(
                    _filter(_v, rawExpr="$b.location.locationName")
                )  # from line 84, col 14.
            write(
                """'<br /></b>
</td>
"""
            )
            # <td>
            # add this copy to cart: <input type="checkbox" name="copy_id" value="$b.id" />
            # [add <input style="width:80px;"type="text" length="3" name="select_x_like_$b.id" value="" /> copies like this to cart]
            # </td>
            write(
                """</tr>
</table>
</div>
"""
            )
        write(
            """<input class="submit" type="submit" name="addtocart" value="Collect selected copies" /> <br /> <!--<br />
<input class="submit" type="submit" name="delete" onclick="return confirm(\'Are you sure?\');" value="Delete selected copies" />-->
</form>

"""
        )
        # show category records. Each is editable in its own category edit template
        write(
            """<h2>Keywords::</h2>
"""
        )
        for c in VFFSL(SL, "title.categorys", True):  # generated from line 100, col 1
            write("""<div class="listing"><span class="listing">""")
            _v = VFFSL(
                SL, "c.categoryName", True
            )  # '$c.categoryName' on line 101, col 44
            if _v is not None:
                write(_filter(_v, rawExpr="$c.categoryName"))  # from line 101, col 44.
            write("""</span><a class="listinglink" href="/categoryedit?id=""")
            _v = VFFSL(SL, "c.id", True)  # '$c.id' on line 101, col 112
            if _v is not None:
                write(_filter(_v, rawExpr="$c.id"))  # from line 101, col 112.
            write(
                """">edit</a></div>
"""
            )
        write(
            """


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

        # edit information for a particular title
        # linked classes, like author and book appear and
        # are editable by links to thier own templates
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

    _mainCheetahMethod_for_TitleEditTemplate = "writeBody"


## END CLASS DEFINITION

if not hasattr(TitleEditTemplate, "_initCheetahAttributes"):
    templateAPIClass = getattr(TitleEditTemplate, "_CHEETAH_templateClass", Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(TitleEditTemplate)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://cheetahtemplate.org/

##################################################
## if run from command line:
if __name__ == "__main__":
    from Cheetah.TemplateCmdLineIface import CmdLineIface

    CmdLineIface(templateObj=TitleEditTemplate()).run()
