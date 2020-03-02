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
__CHEETAH_genTime__ = 1510105566.074614
__CHEETAH_genTimestamp__ = "Wed Nov  8 01:46:06 2017"
__CHEETAH_src__ = "SearchTemplate.tmpl"
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


class SearchTemplate(Skeleton):

    ##################################################
    ## CHEETAH GENERATED METHODS

    def __init__(self, *args, **KWs):

        super(SearchTemplate, self).__init__(*args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = "searchList namespaces filter filtersLib errorCatcher".split()
            for k, v in KWs.items():
                if k in allowedKWs:
                    cheetahKWArgs[k] = v
            self._initCheetahInstance(**cheetahKWArgs)

    def pagetitle(self, **KWS):

        ## CHEETAH: generated from #def pagetitle at line 6, col 1.
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
            """Search the inventory
"""
        )

        ########################################
        ## END - generated method body

        return _dummyTrans and trans.response().getvalue() or ""

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

        write(
            """<script src="/javascript/jquery.fixedheadertable.js"></script>
<script type="text/javascript">
    //Make lesser used fields hideable
    jQuery(document).ready( function(){
        jQuery(\'#sold_begin_date,#sold_end_date,#inv_begin_date,#inv_end_date\').datepicker({dateFormat:\'yy-mm-dd\'}).blur();
        var resultsTable = jQuery(\'#results_table\').dataTable({    \'aSorting\':[[1, \'asc\']],
                                                \'sPaginationType\':\'simple_numbers\',
                                                \'columnDefs\': [
                                                    { targets: [0], visible: false},
                                                ],
                                                "bJQueryUI": true,
                                                "bAutoWidth":true,
                                                "order":[[1, \'asc\']],
                                                "iDisplayLength": 50,
                                                "scrollX": 100,
                                                "sDom": \'<"top"lf>rt<"bottom"ip><"clear">\'
                                                });
        
        //.showHideSearchForm hidden 
        jQuery(".showHideSearchForm").hide();
        
        //this is where we open/close disclosure triangle
        //array is open/closed options for span class
        var disclosureTriContent = [\'<span class="show_hide_disc_triangle ui-state-default ui-corner-all" data-subscript="0"><span class="ui-icon ui-icon-triangle-1-e"></span><span class="text" style="display: block; ">More options...</span></span>\',
            \'<span class="show_hide_disc_triangle ui-state-default ui-corner-all" data-subscript="1"><span class="ui-icon ui-icon-triangle-1-s"></span><span class="text" style="display: block; ">Fewer options...</span></span>\'];

        //start out with .slidingDiv hidden
        jQuery(".slidingDiv").hide();
        jQuery(".show_hide_disc_triangle").show();
        jQuery(\'.show_hide_div\').click(function(){
            //slidetoggle hides/shows div
            jQuery(".slidingDiv").slideToggle();
            //swap out label on show/hide fields button
            jQuery(this).html(disclosureTriContent[(jQuery(this).find(\'.show_hide_disc_triangle\').data(\'subscript\') + 1) % 2]);
            jQuery(this).find(\'.show_hide_disc_triangle\').show();
            return false
        });

        //hide book id column -- now uses datatable to hideq
        //jQuery(\'#results_table td:last-child, #results_table th:last-child\').hide();
        
        //open title edit. Desktops open on doubleclick.
        //IOS & android use single click.
        if (navigator.userAgent.match(/ipad|iphone|ios|android/i) == null) {
            jQuery(\'#results_table tr\').dblclick(function(event) {
                    event.preventDefault();
                    var position = resultsTable.fnGetPosition(this); // getting the clicked row position
                    var titleID = resultsTable.fnGetData(position)[0];
                    document.location.href= \'/titleedit?id=\' + titleID;
                    return false;
            });
        } else {
            jQuery(\'#results_table tr\').click(function(event) {
                    event.preventDefault();
                    var position = resultsTable.fnGetPosition(this); // getting the clicked row position
                    var titleID = resultsTable.fnGetData(position)[0];
                    document.location.href= \'/titleedit?id=\' + titleID;
                    return false;
            });
        }

    });
</script>
"""
        )

        ########################################
        ## END - generated method body

        return _dummyTrans and trans.response().getvalue() or ""

    def body(self, **KWS):

        ## CHEETAH: generated from #def body at line 76, col 1.
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
            """<h1>Inventory</h1>
<div class="showhide"><a  href="javascript:show_hide(\'search_form\')">Show/hide search form</a></div>
<br />
<form id="search_form" method="get" action="/search"
"""
        )
        if not (VFFSL(SL, "empty", True)):  # generated from line 81, col 1
            write(
                """style="visibility:hidden;display:none"
"""
            )
        write(
            '''>

<label class="textbox" for="title">Title</label> 
<input class="textbox" type="text" id="title" name="title" value="'''
        )
        _v = VFFSL(SL, "title", True)  # '$title' on line 87, col 67
        if _v is not None:
            write(_filter(_v, rawExpr="$title"))  # from line 87, col 67.
        write(
            '''" /><br />

<label class="textbox" for="author">Author</label> 
<input class="textbox" type="text" name="author" id="author" value="'''
        )
        _v = VFFSL(SL, "author", True)  # '$author' on line 90, col 69
        if _v is not None:
            write(_filter(_v, rawExpr="$author"))  # from line 90, col 69.
        write(
            '''" /><br />

<label class="textbox" for="category">Keyword</label> 
<input class="textbox" type="text" name="category" id="category" value="'''
        )
        _v = VFFSL(SL, "category", True)  # '$category' on line 93, col 73
        if _v is not None:
            write(_filter(_v, rawExpr="$category"))  # from line 93, col 73.
        write(
            '''" /><br />

<label class="textbox" for="isbn">ISBN</label> 
<input class="textbox" type="text" name="isbn" id="isbn" value="'''
        )
        _v = VFFSL(SL, "isbn", True)  # '$isbn' on line 96, col 65
        if _v is not None:
            write(_filter(_v, rawExpr="$isbn"))  # from line 96, col 65.
        write(
            """" /><br />

<div class=\'show_hide_div\'>
<span class="show_hide_disc_triangle ui-state-default ui-corner-all" data-subscript="0"><span class="ui-icon ui-icon-triangle-1-e"></span><span class="text" style="display: block; ">More options...</span></span>
</div>
<div class="slidingDiv">

<label class="textbox" for="location">Location</label> 
<select class="textbox" id="location" name="location">
"""
        )
        i = 0
        for loc in VFFSL(SL, "locations", True):  # generated from line 106, col 1
            write("""<option id=""")
            _v = VFFSL(SL, "i", True)  # '$i' on line 107, col 12
            if _v is not None:
                write(_filter(_v, rawExpr="$i"))  # from line 107, col 12.
            write(""" value='""")
            _v = VFFSL(SL, "loc.id", True)  # '$loc.id' on line 107, col 22
            if _v is not None:
                write(_filter(_v, rawExpr="$loc.id"))  # from line 107, col 22.
            write(
                """' 
"""
            )
            if "%s" % (VFFSL(SL, "loc.id", True)) == VFFSL(
                SL, "location", True
            ):  # generated from line 108, col 1
                write(
                    """selected="true" 
"""
                )
            write(""">""")
            _v = VFFSL(
                SL, "loc.locationName", True
            )  # '$loc.locationName' on line 111, col 2
            if _v is not None:
                write(_filter(_v, rawExpr="$loc.locationName"))  # from line 111, col 2.
            write(
                """</option>
"""
            )
            i = VFFSL(SL, "i", True) + 1
        write(
            '''</select><br />

<label class="textbox" for="publisher">Publisher</label> 
<input class="textbox" type="text" name="publisher" id="publisher" value="'''
        )
        _v = VFFSL(SL, "publisher", True)  # '$publisher' on line 117, col 75
        if _v is not None:
            write(_filter(_v, rawExpr="$publisher"))  # from line 117, col 75.
        write(
            '''" /><br />

<label class="textbox" for="distributor">Distributor</label> 
<input class="textbox" type="text" name="distributor" id="distributor" value="'''
        )
        _v = VFFSL(SL, "distributor", True)  # '$distributor' on line 120, col 79
        if _v is not None:
            write(_filter(_v, rawExpr="$distributor"))  # from line 120, col 79.
        write(
            '''" /><br />

<label class="textbox" for="owner">Owner</label> 
<input class="textbox" type="text" name="owner" id="owner" value="'''
        )
        _v = VFFSL(SL, "owner", True)  # '$owner' on line 123, col 67
        if _v is not None:
            write(_filter(_v, rawExpr="$owner"))  # from line 123, col 67.
        write(
            """" /><br />


<label class="textbox" for="out_of_stock">Only return out of stock books?</label>

<fieldset id="out_of_stock">
no <input type="radio" name="out_of_stock" id="out_of_stock_no" value="no" 
"""
        )
        if VFFSL(SL, "out_of_stock", True) == "no":  # generated from line 130, col 1
            write(
                """checked
"""
            )
        write(
            """> 
yes<input type="radio" name="out_of_stock" id="out_of_stock_yes" value="yes"
"""
        )
        if VFFSL(SL, "out_of_stock", True) == "yes":  # generated from line 135, col 1
            write(
                """checked
"""
            )
        write(
            '''>
</fieldset>

<br />


<label class="textbox" for="stock_less_than">This many or less in stock</label> 
<input class="textbox" type="text" name="stock_less_than" id="stock_less_than" value="'''
        )
        _v = VFFSL(
            SL, "stock_less_than", True
        )  # '$stock_less_than' on line 145, col 87
        if _v is not None:
            write(_filter(_v, rawExpr="$stock_less_than"))  # from line 145, col 87.
        write(
            '''" /><br />

<label class="textbox" for="stock_more_than">This many or more in stock</label> 
<input class="textbox" type="text" name="stock_more_than" id="stock_more_than" value="'''
        )
        _v = VFFSL(
            SL, "stock_more_than", True
        )  # '$stock_more_than' on line 148, col 87
        if _v is not None:
            write(_filter(_v, rawExpr="$stock_more_than"))  # from line 148, col 87.
        write(
            '''" /><br />

<label class="textbox" for="sold_more_than">This many or more sold</label> 
<input class="textbox" type="text" name="sold_more_than" id="sold_more_than"  value="'''
        )
        _v = VFFSL(SL, "sold_more_than", True)  # '$sold_more_than' on line 151, col 86
        if _v is not None:
            write(_filter(_v, rawExpr="$sold_more_than"))  # from line 151, col 86.
        write(
            '''" /><br />

<label class=\'textbox\' for=\'sold_begin_date\'>This item sold After:</label>
<input type=\'text\' class=\'textbox\' name=\'sold_begin_date\' id=\'sold_begin_date\' value="'''
        )
        _v = VFFSL(
            SL, "sold_begin_date", True
        )  # '${sold_begin_date}' on line 154, col 87
        if _v is not None:
            write(_filter(_v, rawExpr="${sold_begin_date}"))  # from line 154, col 87.
        write(
            '''"/><br />

<label class=\'textbox\' for=\'sold_end_date\'>This item sold Before</label>
<input type=\'text\' class=\'textbox\' name=\'sold_end_date\' id=\'sold_end_date\' value="'''
        )
        _v = VFFSL(SL, "sold_end_date", True)  # '${sold_end_date}' on line 157, col 83
        if _v is not None:
            write(_filter(_v, rawExpr="${sold_end_date}"))  # from line 157, col 83.
        write(
            '''"/><br />

<label class=\'textbox\' for=\'inv_begin_date\'>This item inventoried After:</label>
<input type=\'text\' class=\'textbox\' name=\'inv_begin_date\' id=\'inv_begin_date\' value="'''
        )
        _v = VFFSL(
            SL, "inv_begin_date", True
        )  # '${inv_begin_date}' on line 160, col 85
        if _v is not None:
            write(_filter(_v, rawExpr="${inv_begin_date}"))  # from line 160, col 85.
        write(
            '''"/><br />

<label class=\'textbox\' for=\'inv_end_date\'>This item inventoried Before</label>
<input type=\'text\' class=\'textbox\' name=\'inv_end_date\' id=\'inv_end_date\' value="'''
        )
        _v = VFFSL(SL, "inv_end_date", True)  # '${inv_end_date}' on line 163, col 81
        if _v is not None:
            write(_filter(_v, rawExpr="${inv_end_date}"))  # from line 163, col 81.
        write(
            '''"/><br />

<label class="textbox" for="tag">Tag</label> 
<input class="textbox" type="text" id="tag" name="tag" value="'''
        )
        _v = VFFSL(SL, "tag", True)  # '$tag' on line 166, col 63
        if _v is not None:
            write(_filter(_v, rawExpr="$tag"))  # from line 166, col 63.
        write(
            """" /><br />

<label class="textbox" for="formatType">Format</label> 
<select class="textbox" id="formatType" name="formatType">

"""
        )
        for f in VFFSL(SL, "formats", True):  # generated from line 171, col 1
            write("""<option value='""")
            _v = VFFSL(SL, "f", True)  # '$f' on line 172, col 16
            if _v is not None:
                write(_filter(_v, rawExpr="$f"))  # from line 172, col 16.
            write(
                """' 
"""
            )
            # if $f==$formatType
            # selected="true"
            # end if
            write(""">""")
            _v = VFFSL(SL, "f", True)  # '$f' on line 176, col 2
            if _v is not None:
                write(_filter(_v, rawExpr="$f"))  # from line 176, col 2.
            write(
                """</option>
"""
            )
        write(
            """</select><br />
</div>
<br />
<label class="textbox" for="kind">Kind</label> 
<select class="textbox" id="kind" name="kind">
"""
        )
        for k in VFFSL(SL, "kinds", True):  # generated from line 183, col 1
            write("""<option value='""")
            _v = VFFSL(SL, "k.id", True)  # '$k.id' on line 184, col 16
            if _v is not None:
                write(_filter(_v, rawExpr="$k.id"))  # from line 184, col 16.
            write(
                """' 
"""
            )
            if "%s" % (VFFSL(SL, "k.id", True)) == VFFSL(
                SL, "kind", True
            ):  # generated from line 185, col 1
                write(
                    """selected="true" 
"""
                )
            write(""">""")
            _v = VFFSL(SL, "k.kindName", True)  # '$k.kindName' on line 188, col 2
            if _v is not None:
                write(_filter(_v, rawExpr="$k.kindName"))  # from line 188, col 2.
            write(
                """</option>
"""
            )
        write(
            """</select><br />

<input class="submit" type="submit">

<br />
</form>
<form action="/titlelist" method="get" >
<table class="sortable" id="results_table" >
<thead>
  <tr>
    <th>ID</th>
    <th>Mark</th>
"""
        )
        if VFFSL(SL, "should_show_images", True):  # generated from line 202, col 5
            write(
                """    <th>Image</th>
"""
            )
        write(
            """    <th>Title</th>
    <th>Author</th>
    <th>Format</th>
    <th>Copies in Stock</th>
    <th>Copies Sold</th>
    <th>Distributor</th>
    <th>Publisher</th>
    <th>First Inventoried</th>
    <th>Latest Inventoried</th>
    <th>First Sold</th>
    <th>Last Sold</th>
  </tr>
</thead>
<tbody>
"""
        )
        for t in VFFSL(SL, "titles", True):  # generated from line 219, col 1
            try:  # generated from line 220, col 5
                write(
                    """      <tr>
      <td>"""
                )
                _v = VFFSL(SL, "t.id", True)  # '$t.id' on line 222, col 11
                if _v is not None:
                    write(_filter(_v, rawExpr="$t.id"))  # from line 222, col 11.
                write(
                    ''' </td>
      <td><input type="checkbox" name="titles" value="'''
                )
                _v = VFFSL(SL, "t.id", True)  # '$t.id' on line 223, col 55
                if _v is not None:
                    write(_filter(_v, rawExpr="$t.id"))  # from line 223, col 55.
                write(
                    """" onclick=\'if (event.stopPropagation){
                   event.stopPropagation();
               }
               else if(window.event){
                  window.event.cancelBubble=true;
               }\'/></td>
"""
                )
                if VFFSL(
                    SL, "should_show_images", True
                ):  # generated from line 229, col 9
                    write(
                        """        <td>
"""
                    )
                    if VFFSL(SL, "t.images", True):  # generated from line 231, col 13
                        if VFN(
                            VFFSL(SL, "t.images", True), "retrieve_image_url", False
                        )(
                            "small"
                        ):  # generated from line 232, col 17
                            write("""                    <img src='""")
                            _v = VFN(
                                VFFSL(SL, "t.images", True), "retrieve_image_url", False
                            )(
                                "small"
                            )  # '$t.images.retrieve_image_url("small")' on line 233, col 31
                            if _v is not None:
                                write(
                                    _filter(
                                        _v,
                                        rawExpr='$t.images.retrieve_image_url("small")',
                                    )
                                )  # from line 233, col 31.
                            write(
                                """'>
"""
                            )
                    write(
                        """        </td>
"""
                    )
                write("""        <td>""")
                if VFN(VFFSL(SL, "t", True), "safe", False)(
                    "booktitle"
                ):  # generated from line 238, col 13
                    _v = VFN(VFFSL(SL, "t", True), "safe", False)("booktitle")
                    if _v is not None:
                        write(_filter(_v))
                else:
                    _v = ""
                    if _v is not None:
                        write(_filter(_v))
                write(
                    """</td>
        <td>"""
                )
                if VFN(
                    VFFSL(SL, "t", True), "authors_as_string", False
                )():  # generated from line 239, col 13
                    _v = VFN(VFFSL(SL, "t", True), "authors_as_string", False)()
                    if _v is not None:
                        write(_filter(_v))
                else:
                    _v = ""
                    if _v is not None:
                        write(_filter(_v))
                write(
                    """</td>
        <td>"""
                )
                if VFFSL(SL, "t.type", True):  # generated from line 240, col 13
                    _v = VFFSL(SL, "t.type", True)
                    if _v is not None:
                        write(_filter(_v))
                else:
                    _v = ""
                    if _v is not None:
                        write(_filter(_v))
                write(
                    """</td>
        <td>"""
                )
                if VFN(VFFSL(SL, "t", True), "copies_in_status", False)(
                    "STOCK"
                ):  # generated from line 241, col 13
                    _v = VFN(VFFSL(SL, "t", True), "copies_in_status", False)("STOCK")
                    if _v is not None:
                        write(_filter(_v))
                else:
                    _v = "0"
                    if _v is not None:
                        write(_filter(_v))
                write(
                    """</td>
        <td>"""
                )
                if VFN(VFFSL(SL, "t", True), "copies_in_status", False)(
                    "SOLD"
                ):  # generated from line 242, col 13
                    _v = VFN(VFFSL(SL, "t", True), "copies_in_status", False)("SOLD")
                    if _v is not None:
                        write(_filter(_v))
                else:
                    _v = "0"
                    if _v is not None:
                        write(_filter(_v))
                write(
                    """</td>
        <td>"""
                )
                if VFN(
                    VFFSL(SL, "t", True), "distributors_as_string", False
                )():  # generated from line 243, col 13
                    _v = VFN(VFFSL(SL, "t", True), "distributors_as_string", False)()
                    if _v is not None:
                        write(_filter(_v))
                else:
                    _v = ""
                    if _v is not None:
                        write(_filter(_v))
                write(
                    """</td>
        <td>"""
                )
                if VFN(VFFSL(SL, "t", True), "safe", False)(
                    "publisher"
                ):  # generated from line 244, col 13
                    _v = VFN(VFFSL(SL, "t", True), "safe", False)("publisher")
                    if _v is not None:
                        write(_filter(_v))
                else:
                    _v = ""
                    if _v is not None:
                        write(_filter(_v))
                write(
                    """</td>
        <td>"""
                )
                if VFFSL(
                    SL, "t.first_book_inventoried", True
                ):  # generated from line 245, col 13
                    _v = VFFSL(SL, "t.first_book_inventoried.inventoried_when", True)
                    if _v is not None:
                        write(_filter(_v))
                else:
                    _v = ""
                    if _v is not None:
                        write(_filter(_v))
                write(
                    """</td>
        <td>"""
                )
                if VFFSL(
                    SL, "t.last_book_inventoried", True
                ):  # generated from line 246, col 13
                    _v = VFFSL(SL, "t.last_book_inventoried.inventoried_when", True)
                    if _v is not None:
                        write(_filter(_v))
                else:
                    _v = ""
                    if _v is not None:
                        write(_filter(_v))
                write(
                    """</td>
        <td>"""
                )
                if VFFSL(
                    SL, "t.first_book_sold", True
                ):  # generated from line 247, col 13
                    _v = VFFSL(SL, "t.first_book_sold.sold_when", True)
                    if _v is not None:
                        write(_filter(_v))
                else:
                    _v = ""
                    if _v is not None:
                        write(_filter(_v))
                write(
                    """</td>
        <td>"""
                )
                if VFFSL(
                    SL, "t.last_book_sold", True
                ):  # generated from line 248, col 13
                    _v = VFFSL(SL, "t.last_book_sold.sold_when", True)
                    if _v is not None:
                        write(_filter(_v))
                else:
                    _v = ""
                    if _v is not None:
                        write(_filter(_v))
                write(
                    """</td>
      </tr>
"""
                )
            except:  # generated from line 250, col 5
                write(
                    """        pass
"""
                )
        write(
            """</tbody>
</table>
<br />
<input class="submit"  name="list" type="submit" value="get marked titles" /><br /><br />
<input class="submit"  name="delete" onclick="return confirm(\'Are you sure?\');" type="submit" value="delete marked titles" />
</form>

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

        # Search the inventory and return table of results
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

    _mainCheetahMethod_for_SearchTemplate = "writeBody"


## END CLASS DEFINITION

if not hasattr(SearchTemplate, "_initCheetahAttributes"):
    templateAPIClass = getattr(SearchTemplate, "_CHEETAH_templateClass", Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(SearchTemplate)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://cheetahtemplate.org/

##################################################
## if run from command line:
if __name__ == "__main__":
    from Cheetah.TemplateCmdLineIface import CmdLineIface

    CmdLineIface(templateObj=SearchTemplate()).run()
