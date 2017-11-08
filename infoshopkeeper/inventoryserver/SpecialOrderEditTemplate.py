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
from Cheetah.compat import unicode
from inventoryserver.Skeleton import Skeleton

##################################################
## MODULE CONSTANTS
VFFSL=valueFromFrameOrSearchList
VFSL=valueFromSearchList
VFN=valueForName
currentTime=time.time
__CHEETAH_version__ = '3.0.0'
__CHEETAH_versionTuple__ = (3, 0, 0, 'final', 1)
__CHEETAH_genTime__ = 1510105566.1317282
__CHEETAH_genTimestamp__ = 'Wed Nov  8 01:46:06 2017'
__CHEETAH_src__ = 'SpecialOrderEditTemplate.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Nov  8 00:51:24 2017'
__CHEETAH_docstring__ = 'Autogenerated by Cheetah: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class SpecialOrderEditTemplate(Skeleton):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        super(SpecialOrderEditTemplate, self).__init__(*args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = 'searchList namespaces filter filtersLib errorCatcher'.split()
            for k,v in KWs.items():
                if k in allowedKWs: cheetahKWArgs[k] = v
            self._initCheetahInstance(**cheetahKWArgs)
        

    def pagetitle(self, **KWS):



        ## CHEETAH: generated from #def pagetitle at line 6, col 1.
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
        
        if VFFSL(SL,"specialorder.customerName",True): # generated from line 7, col 5
            write('''    Editing specialorder for  ''')
            _v = VFFSL(SL,"specialorder.customerName",True) # '$specialorder.customerName' on line 8, col 31
            if _v is not None: write(_filter(_v, rawExpr='$specialorder.customerName')) # from line 8, col 31.
            write('''
''')
        else: # generated from line 9, col 5
            write('''    Editing new special order
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def headscripts(self, **KWS):



        ## CHEETAH: generated from #def headscripts at line 14, col 1.
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
        
        write('''<script type="text/javascript" src="/javascript/jquery.validate.min.js"></script>
<script type="text/javascript">
    jQuery(document).ready( function(){
        var inventory_data={};

        //add validator
        jQuery(\'form\').validate({
            rules: {
                        customerName: "required",
                        customerEmail: {
                            required: "#id_customerPhoneNumber:blank",
                            email: true
                        },
                        customerPhoneNumber: {
                            required: "#id_customerEmail:blank",
                            phoneUS: true
                        }
                    },
            messages:   {
                customerName: "Customer Name is required",
                customerEmail: "Customer Email or Phone Number is required",
                customerPhoneNumber: "Customer Email or Phone Number is required"
            }
        });
        
        var dlg=jQuery(\'#new_special_order_dialog\').dialog( {
            autoOpen: false,
            modal: true,
            open: function(event, ui) {
                console.log(\'opening dialog\');
            },
            //void isbn field
            //void list of attributes (title, price, etc)
            //of transaction.
            close: function() {
                inventory_data={};
                jQuery(this).find(\'.isbnfield\').val(\'\');
                jQuery(this).find(\'.title_list\').children().remove();
            },
            buttons: {
                //close button
                Cancel: function(){
                    dlg.dialog(\'close\');
                },
                //if you approve of the results from the isbn search,
                //add them to the cart
                \'Special Order\': function(){

                    //add item to cart table
                    //Should be ajax update
                    //Only if there\'s really an item.
                    if (Object.keys(inventory_data).length > 0 ) {
                        console.log(\'in add_to_special_order\')
                        
                        //add item to special order, and update page if it succeeds
                        itemargs={\'item\':JSON.stringify(inventory_data), \'specialOrderID\':jQuery(\'#sqlobject_id\').val()};
                        jQuery.post(\'/specialorder/add_to_special_order\', itemargs, function(){
                            console.log(inventory_data);
                            //special_order_string=\'<li class=\\\'special_order_item_list\\\'><ul><li>\' + inventory_data.id + \'</li><li>\' +inventory_data.isbn + \'</li><li>\' + inventory_data.title+ + \'</li><li>\' + inventory_data.authors_as_string + \'</li><li><button onclick=\\"window.location.href=\\\'\\/specialorder\\/special_order_item_edit?id=\' + inventory_data.id + \'\\">edit</button</ul></li>\'                         //<li><button onclick=\\"window.location.href=\\\'/specialorder/special_order_item_edit?id=\'inventory_data.id\'\\">edit</button></li></ul></li>\';
                            //jQuery(\'#special_order_list\').append(special_order_string);                           
                            location.reload();
                            dlg.dialog(\'close\');
                        });
                    }
                    return false;
                }
            }
        });
        
        //jquery alert dialog for when isbn
        //not found in database
        jQuery( "#isbn_not_found_error" ).dialog({
            autoOpen: false,
            modal: true,
            buttons: {
                Ok: function() {
                    jQuery(this).dialog( \'close\' );
                    return false;
                }
            }
        });        
        
        //add button to make new special order
        jQuery(\'#new_special_order_item\').button().click( function( event ) {
            event.preventDefault();
            dlg.dialog(\'open\');
            return false;
         });
         
        //listener function to search database for isbn
        //and return item info and info applicable to transaction
        //i.e., if its taxable
        isbn_listener = function(evt) {

            var event_target=jQuery(evt.target)
            var isbnstring=event_target.val();
            var title_list=event_target.closest(\'div\').find(\'.title_list\')
            //cache isbn_not_found dialog
            var isbn_error_alert=event_target.closest(\'body\').find(\'#isbn_not_found_error\');
            isbnstring=isbnstring.toLowerCase();
            isbnstring=isbnstring.replace(/\\s+/g, \' \');

            //scrub isbn of spaces and hyphens if it is a potential 
            //real isbn
            if (isbnstring.length>11) {
                isbnstring=isbnstring.replace(/[\\s-]/g, \'\');
            }
            
            //if there\'s an isbn, then search database for it.
            if (isbnstring.length>0) {
                if (isbnstring.match( /\\d{13}|\\d{12}|\\d{9}[0-9xX]{1}/ )) {
                    console.log(\'isbn will try to search\');

                    jQuery.getJSON( \'/search_isbn\', {\'isbn\':isbnstring}, function(inventory_data1){
                        inventory_data1[0];
                        inventory_data=inventory_data1[0];

                        console.log(inventory_data1);
                        
                        //if item is an inventoried item and there\'s a real result
                        //add all item info to dialog so user can approve add
                        //to inventory or not. If no results, open isbn error alert.
                        if ((inventory_data !== undefined) && (inventory_data.title !==undefined)) {
                            title_list.empty();
                            title_list.append(\'<li>\'+inventory_data.title+\'</li><li>\'+ inventory_data.authors_as_string +\'</li>\');
                        } else {
                            isbn_error_alert.dialog(\'open\');
                        }
                    });
                } else {
                    window.open(\'/specialorder/select_special_order_search?authorOrTitle=\'+escape(isbnstring) + \'&special_order=\' + jQuery(\'#sqlobject_id\').val(), \'_self\');
                }  
            } 

            if ( event_target.val() != isbnstring) {
                event_target.val(isbnstring);
            }
            
            evt.preventDefault();
            return false;
        }
        
        //prevent return from triggering submit.
        //we want to actually approve the data before we submit.
        jQuery(\'.isbnfield\').keypress( function(evt) {
            if (evt.keyCode == 13) {
                console.log(\'in key press traps return\');
                jQuery(this).closest(\'.ui-dialog\').find(\'.ui-button\')[1].focus();
                isbn_listener(evt);
                evt.preventDefault();
            }
        });
    });
</script
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def body(self, **KWS):



        ## CHEETAH: generated from #def body at line 171, col 1.
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
        
        if VFFSL(SL,"specialorder.customerName",True): # generated from line 172, col 1
            write('''    <h1>Special Order record for ''')
            _v = VFFSL(SL,"specialorder.customerName",True) # '${specialorder.customerName}' on line 173, col 34
            if _v is not None: write(_filter(_v, rawExpr='${specialorder.customerName}')) # from line 173, col 34.
            write('''</h1>
''')
        else: # generated from line 174, col 1
            write('''    <h1>New Special Order</h1>
''')
        write('''
<form class=\'editform\' method="get" action="/specialorder/special_order_edit">
''')
        _v = VFFSL(SL,"specialorder.object_to_form",True) # '$specialorder.object_to_form' on line 179, col 1
        if _v is not None: write(_filter(_v, rawExpr='$specialorder.object_to_form')) # from line 179, col 1.
        write('''
</form></br>

''')
        if VFFSL(SL,"specialorder.titles",True): # generated from line 182, col 1
            write('''    <h2>Inventoried items special ordered</h2>
''')
        write('''
''')
        if VFFSL(SL,"specialorder.customerName",True): # generated from line 186, col 1
            write("""<div id='new_special_order_group'>
    <button id='new_special_order_item' class='new_special_order_item'>New Item</button></br>
    <div id='new_special_order_dialog' class='new_special_order_dialog' title='Enter ISBN, Author/Title or Price'>
        <form action='' method='get'>
            <input class='isbnfield' type='text' name='isbn' />""")
            write("""       </form>
       <div id='title_list_panel' class='title_list_panel' name='title_list_panel'>
            <ul id='title_list' class='title_list' name='title_list'></ul>
       </div>  
    </div>
    <div id='isbn_not_found_error' class='error_dialog' title='Error: ISBN not found'>
            Check the ISBN again or use the search button to search the inventory by attributes.
    </div>
</div>
""")
        write('''
''')
        if VFFSL(SL,"specialorder.titles",True): # generated from line 203, col 1
            write("""    <ul id= 'special_order_list' class='special_order_list'>
""")
            for tso in VFFSL(SL,"specialorder.title_pivots",True): # generated from line 205, col 9
                write("""        <li class='special_order_item_list'>
            <ul>
                <li>""")
                if VFFSL(SL,"tso.id",True) : # generated from line 208, col 21
                    _v =  VFFSL(SL,"tso.id",True) 
                    if _v is not None: write(_filter(_v))
                else:
                    _v =  ""
                    if _v is not None: write(_filter(_v))
                write('''</li>
                <li>''')
                if VFFSL(SL,"tso.title.isbn",True) : # generated from line 209, col 21
                    _v =  VFFSL(SL,"tso.title.isbn",True) 
                    if _v is not None: write(_filter(_v))
                else:
                    _v =  ""
                    if _v is not None: write(_filter(_v))
                write('''</li>
                <li>''')
                if VFFSL(SL,"tso.title.booktitle",True) : # generated from line 210, col 21
                    _v =  VFFSL(SL,"tso.title.booktitle",True) 
                    if _v is not None: write(_filter(_v))
                else:
                    _v =  ""
                    if _v is not None: write(_filter(_v))
                write('''</li>
                <li>''')
                if VFFSL(SL,"tso.title.authors_as_string",True) : # generated from line 211, col 21
                    _v =  VFFSL(SL,"tso.title.authors_as_string",True) 
                    if _v is not None: write(_filter(_v))
                else:
                    _v =  ""
                    if _v is not None: write(_filter(_v))
                write('''</li>
                <li>''')
                if VFFSL(SL,"tso.orderStatus",True) : # generated from line 212, col 21
                    _v =  VFFSL(SL,"tso.orderStatus",True) 
                    if _v is not None: write(_filter(_v))
                else:
                    _v =  ""
                    if _v is not None: write(_filter(_v))
                write('''</li>
                <li><button onclick="window.location.href=\'/specialorder/special_order_item_edit?id=''')
                _v = VFFSL(SL,"tso.id",True) # '$tso.id' on line 213, col 101
                if _v is not None: write(_filter(_v, rawExpr='$tso.id')) # from line 213, col 101.
                write('''\'">edit</button></li>
            </ul>
''')
            write('''        </li>
    </ul>
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
        
        # Edit Special Order information
        write('''



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

    _mainCheetahMethod_for_SpecialOrderEditTemplate= 'writeBody'

## END CLASS DEFINITION

if not hasattr(SpecialOrderEditTemplate, '_initCheetahAttributes'):
    templateAPIClass = getattr(SpecialOrderEditTemplate, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(SpecialOrderEditTemplate)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://cheetahtemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=SpecialOrderEditTemplate()).run()


