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
from Skeleton import Skeleton
from config.etc import departments

##################################################
## MODULE CONSTANTS
VFFSL = valueFromFrameOrSearchList
VFSL = valueFromSearchList
VFN = valueForName
currentTime = time.time
__CHEETAH_version__ = "3.0.0"
__CHEETAH_versionTuple__ = (3, 0, 0, "final", 1)
__CHEETAH_genTime__ = 1510105565.826558
__CHEETAH_genTimestamp__ = "Wed Nov  8 01:46:05 2017"
__CHEETAH_src__ = "CartTemplate2.tmpl"
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


class CartTemplate2(Skeleton):

    ##################################################
    ## CHEETAH GENERATED METHODS

    def __init__(self, *args, **KWs):

        super(CartTemplate2, self).__init__(*args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = "searchList namespaces filter filtersLib errorCatcher".split()
            for k, v in KWs.items():
                if k in allowedKWs:
                    cheetahKWArgs[k] = v
            self._initCheetahInstance(**cheetahKWArgs)

    def headscripts(self, **KWS):

        ## CHEETAH: generated from #def headscripts at line 3, col 1.
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
            """<script type=\'text/javascript\'>                                         
    jQuery(document).ready( function(){
        var inventory_data={};
        var inventory_data1={};
        var price;
        var price_array;
        var titleID;
        var inventory_data_dict;
        var isbn_dialog;
                
        //set up ajax error handling
//         jQuery.ajaxSetup({  \'cache\':false,
//                             \'error\':function(XMLHttpRequest,textStatus, errorThrown) {   
//                                 alert(textStatus + \'\\r\' +
//                                       errorThrown + \'\\r\' +
//                                       XMLHttpRequest.responseText);
//                             }
//         });
        
        //jQuery(\'#void-toggle\').button();
        
        //make sure keypress goes to default dialog
        jQuery(document).keydown(function(event) {
            if (  jQuery(\'input:focus\').length == 0 ) {
                //at some point switch to values -- keycodes are not good across all layouts 
                if ((event.keyCode > 47) && (event.keyCode < 58 )) {
                    //event.preventDefault();
                    jQuery(\'#book\').click();
                    jQuery(\'#my-form-book .isbnfield\').focus();
                    jQuery(\'#my-form-book .isbnfield\').trigger(jQuery.Event({type:\'keydown\', which:event.which, keyCode:event.keyCode, charCode:event.charCode}));
                    //return false;
                }
            }            
        
            
            var charPos = event.target.selectionStart;
            var prevPos = jQuery(this).data(\'prevPos\');

            if (typeof event.target.value !== "undefined") {
                var strLength = event.target.value.length;
            } else {
                var strLength = 0;
            }

            if(event.which==39){
                        //only go right if we really reached the end, that means the prev pos is the same then the current pos
                if(charPos==strLength && (prevPos ==null || prevPos == charPos)){
                    jQuery(this).next().focus();
                    jQuery(this).data(\'prevPos\',null);
                }else{
                    jQuery(this).data(\'prevPos\',charPos);
                }
            } else if (event.which==37){
            //only go left if we really reached the beginning, that means the prev pos is the same then the current pos
                if(charPos == 0 && (prevPos ==null || prevPos == charPos)){
                    jQuery(this).prev().focus();
                    jQuery(this).data(\'prevPos\',null);
                }else{
                    jQuery(this).data(\'prevPos\',charPos);
                }
            } else if (event.which==40){
                jQuery(this).next().focus();
                jQuery(this).data(\'prevPos\',null);

            }else if(event.which==38){
                jQuery(this).prev().focus();
                jQuery(this).data(\'prevPos\',null);
            }
        });
    
        //add remove this row button from every row
        jQuery( document ).on(\'click\', \'.remove_item\', function(){
            table_row_index=jQuery(this).parent().parent().index();
            jQuery.post(\'/register/remove_item_from_cart\', {index:table_row_index}, function() {
                jQuery(\'table tr:eq(\'+table_row_index+\')\').remove();
            });
            return false;
        });
        
        //check out cart. mark sold. add to transactions, etc
        //remove items from table. Should change this to an ajax
        //reload of table
        jQuery("#check_out").click(function() {
            jQuery.post("/register/check_out", function() {
                jQuery("#cart_table tr").remove();
                return false;
            });
            return false;
        });
        
        //ditch the cart entirely
        //should change this to an ajax call
        jQuery("#void_sale").click(function() {
            jQuery.post("/register/void_cart", function() {
                jQuery("#cart_table tr").remove();
                return false;
            });
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
                
        jQuery( "#price_dialog" ).dialog({
               autoOpen: false, 
               modal: true,
               buttons: {
                  OK: function() {
                        if ( !isNaN(jQuery(\'#price_select\').val()) ) {
                            price = jQuery(\'#price_select option:selected\').text();
                            console.log(price);
                            console.log(inventory_data_dict);
                            inventory_data1=inventory_data_dict[price];
                            console.log(inventory_data1);
                            
                            var title_list=isbn_dialog.find(\'.title_list\');
                            var outer_div=isbn_dialog.find(\'.special_order_div\');
                            var selectbox = outer_div.find(\'select\');   
                                                    
                            //if item is an inventoried item and there\'s a real result
                            //add all item info to dialog so user can approve add
                            //to inventory or not. If no results, open isbn error alert.
                            if (inventory_data1.isInventoried ) {
                                if ((inventory_data1 !== undefined) && (inventory_data1.booktitle !==undefined)) {
                                    console.log(isbn_dialog);
                                    title_list.empty();
                                    title_list.append(\'<li>\'+inventory_data1.department+\'</li><li>\'+inventory_data1.booktitle+\'</li><li>\'+ inventory_data1.ourprice+\'</li>\');
                                    jQuery.extend(inventory_data, inventory_data1);

                                    outer_div.css(\'display\', \'none\');
                                    if (inventory_data1.special_orders != undefined) {
                                        if (inventory_data1.special_orders.length > 0) {
                                              outer_div.css(\'display\', \'block\');
                                              selectbox.empty();
                                              selectbox.append(\'<option selected value="0"></option>\');
                                              jQuery.each(inventory_data1.special_orders, function() {
                                                  selectbox.append(\'<option value="\' + this[0] + \'">\' + this[1] + \'</option>\');
                                              });
                                        }
                                    }
                                } else {
                                    isbn_error_alert.dialog(\'open\');
                                }
                            }
                            jQuery(this).dialog("close");
                        }
                }
            },
        });
                
        //There is a button for every kind of product (books, etc)
        //This dialog adds a dialog to each of them
        //For inventoried items, check isbn. Otherwise, just
        //expect to get price of item. The close handler is because the dialog
        //is permanent rather than recreated each time.
        jQuery(\'.my-forms\').each( function(){
            var dlg=jQuery(this).dialog( {
                autoOpen: false,
                modal: true,
                open: function(event, ui) {
                    isbn_dialog=jQuery(this);
                },
                //void isbn field
                //void list of attributes (title, price, etc)
                //of transaction.
                close: function() {
                    inventory_data={};
                    jQuery(this).find(\'.isbnfield\').val(\'\');
                    jQuery(this).find(\'.title_list\').children().remove();
                    jQuery(this).find(\'input:checkbox\').removeAttr(\'checked\')
                    var so_div=jQuery(this).find(\'.special_order_div\').css(\'display\', \'none\');
                    so_div.find(\'.special_order_data_div\').css(\'display\', \'none\');
                    so_div.find(\'select\').empty();
                    },
                buttons: {
                    //close button
                    Cancel: function(){
                        dlg.dialog(\'close\');
                    },
                    //if you approve of the results from the isbn search,
                    //add them to the cart
                    \'Add to Order\': function(){
                       
                        //add item to cart table
                        //Should be ajax update
                        //Only if there\'s really an item.
                        if (Object.keys(inventory_data).length > 0 ) {
                
                            //if there is a special order chosen, add it to data to post to cart
                            inventory_data[\'special_order_selected\'] = jQuery(this).find(\'.special_order_data_select\').val()
                            //add item to the cart
                            jQuery.post(\'/register/add_item_to_cart\', {item:JSON.stringify(inventory_data)}, function(){
                                jQuery(\'#cart_table > tbody\').append(\'<tr><td>\'+(((typeof  inventory_data.department) != "undefined")?inventory_data.department:\'\')
                                    +\'</td><td>\'+(((typeof inventory_data.booktitle) != \'undefined\')?inventory_data.booktitle:\'\')
                                    + \'</td><td>\'+(((typeof  inventory_data.isbn) != "undefined")?inventory_data.isbn:\'\') 
                                    +\'</td><td>\'+(((typeof  inventory_data.ourprice) != "undefined")?inventory_data.ourprice:\'\')
                                    +\'</td><td><input type="button" class="remove_item" value="Drop from Cart" /></td></tr>\');

                                dlg.dialog(\'close\');
                            });
                        }
                        return false;
                    }
                }
            });
            //connect the dialog and the button
            jQuery(this).parent().siblings(\'.main\').find(\'#\'+jQuery(this).attr(\'data-name\')).click( function() {
                dlg.dialog(\'open\');
                return false;
            });
        });
         
        //listener function to search database for isbn
        //and return item info and info applicable to transaction
        //i.e., if its taxable
        isbn_listener = function(evt) {
            //get category data (isTaxable, isInventoried) from button
            var event_target=jQuery(evt.target)
            var category_data=event_target.parent().parent().data()
            var isbnstring=event_target.val();
            console.log("isbnstring is ", isbnstring);

            var title_list=event_target.closest(\'div\').find(\'.title_list\');
            var outer_div=event_target.closest(\'div\').find(\'.special_order_div\');
            var selectbox = outer_div.find(\'select\');
            
            //cache isbn_not_found dialog
            var isbn_error_alert=event_target.closest(\'body\').find(\'#isbn_not_found_error\');
            isbnstring=isbnstring.toLowerCase();
            isbnstring=isbnstring.replace(/\\s+/g, \' \');

            //scrub isbn of spaces and hyphens if it is a potential 
            //real isbn
            if (isbnstring.match(/(\\d([\\s-]*)){12,13}|(\\d([\\s-]*)){15,18}|([\\dxX]([\\s-]*)){10}/)) {
                isbnstring=isbnstring.replace(/[\\s-]/g, \'\');
            }
            
            
            //if there\'s an isbn and the category is an inventoried item (book, music, film)
            //search database for it.
            if (isbnstring.length>0 && category_data.is_inventoried_item == \'True\') {

                if (isbnstring.match( /\\d{13}|\\d{12}|\\d{9}[0-9xX]{1}/ )) {
                    
                    //temporarily truncate price until we sticker all sale books
                    if (isbnstring.length == 15 || isbnstring.length==18) {
                        isbnstring=isbnstring.slice(0,-5);
                    }
                        

                    jQuery.getJSON( \'/register/get_item_by_isbn\', {\'isbn\':isbnstring}, function(inventory_data_result){
                        if (category_data.is_inventoried_item && inventory_data_result.length==0){
                            isbn_error_alert.dialog(\'open\');
                            return;
                        }
                        
                        inventory_data_dict=inventory_data_result[0];
                        price_array= jQuery.map(inventory_data_dict, function(value, key) { return key });
                        jQuery.map(inventory_data_dict, function(value, key) {
                            //add category data to inventory data that was found... keeping one dict is easier.
                            jQuery.extend(value, {\'department\':category_data.label, \'isInventoried\':category_data.is_inventoried_item, \'isTaxable\':category_data.is_taxable});
                        });
                        if (price_array.length==1) {
                            //just get first key\'s value
                            inventory_data1=inventory_data_dict[price_array[0]];
                            
                        
                            //if item is an inventoried item and there\'s a real result
                            //add all item info to dialog so user can approve add
                            //to inventory or not. If no results, open isbn error alert.
                            if (category_data.is_inventoried_item ) {
                                if ((inventory_data1 !== undefined) && (inventory_data1.booktitle !==undefined)) {
                                    title_list.empty();
                                    title_list.append(\'<li>\'+category_data.label+\'</li><li>\'+inventory_data1.booktitle+\'</li><li>\'+ inventory_data1.ourprice+\'</li>\');
                                    jQuery.extend(inventory_data, inventory_data1);

                                    outer_div.css(\'display\', \'none\');
                                    if (inventory_data1.special_orders != undefined) {
                                        if (inventory_data1.special_orders.length > 0) {
                                              outer_div.css(\'display\', \'block\');
                                              selectbox.empty();
                                              selectbox.append(\'<option selected value="0"></option>\');
                                              jQuery.each(inventory_data1.special_orders, function() {
                                                  selectbox.append(\'<option value="\' + this[0] + \'">\' + this[1] + \'</option>\');
                                              });
                                        }
                                    }
                                } else {
                                    isbn_error_alert.dialog(\'open\');
                                }
                            }
                        } else {
                            jQuery(\'#price_select\').find(\'option:gt(0)\').remove();
                            jQuery.each(price_array, function(val, text) {
                                jQuery(\'#price_select\').append( jQuery(\'<option></option>\').val(val).html(text) )
                            });
                            jQuery(\'#price_dialog\').dialog(\'open\');
                        }
                    });
                } else {
                    window.open(\'/register/select_item_search?authorOrTitle=\'+escape(isbnstring), \'_self\');
                }  
            
            //if is not inventoried, just add the price & category.
            } else if (isbnstring.length>0 && category_data.is_inventoried_item == \'False\') {
                            title_list.empty();
                            title_list.append(\'<li>\'+category_data.label+\'</li>\');
                            title_list.append(\'<li>\'+isbnstring+\'</li>\');
                            jQuery.extend(inventory_data, {\'department\':category_data.label, \'isInventoried\':category_data.is_inventoried_item, \'isTaxable\':category_data.is_taxable});
                            jQuery.extend(inventory_data, {\'ourprice\': isbnstring });
            }

            if ( event_target.val() != isbnstring) {
                event_target.val(isbnstring);
            }
            
            evt.preventDefault();
            return false;
        }
        
        //add isbn_listener to these isbnfields
        //jQuery(\'.isbnfield\').blur( isbn_listener );
        
        //prevent return from triggering submit.
        //we want to actually approve the data before we submit.
        jQuery(\'.isbnfield\').keypress( function(evt) {
            console.log("keypress " +  jQuery(\'.isbnfield\').val()) 
            if (evt.keyCode == 13 || evt.charCode == 13) {
                console.log(evt)
                evt.preventDefault();

                console.log(\'in key press traps return\');
                console.log(jQuery(this).closest(\'.ui-dialog\').find(\'.ui-button\'));
                jQuery(this).closest(\'.ui-dialog\').find(\'.ui-button\')[2].focus();

                isbn_listener(evt);
            }
        });
        
        jQuery(\'input:checkbox\').change( function() {
            if (jQuery(this).is(\':checked\')) {
                jQuery(this).parent().find(\'div\').css(\'display\', \'block\');
            } else {
                jQuery(this).parent().find(\'div\').css(\'display\', \'none\');
            }
        });
        
    });
</script>
"""
        )

        ########################################
        ## END - generated method body

        return _dummyTrans and trans.response().getvalue() or ""

    def pagetitle(self, **KWS):

        ## Generated from #def pagetitle: Build Cart... at line 363, col 1.
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

        write("""Build Cart...""")

        ########################################
        ## END - generated method body

        return _dummyTrans and trans.response().getvalue() or ""

    def body(self, **KWS):

        ## CHEETAH: generated from #def body at line 365, col 1.
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
            """    <h1>Remove Items from Inventory</h1>
    <div id = 'cart_panel'>
"""
        )
        # <label for='void-toggle'>Void</label>
        # <input type='checkbox' id='void-toggle' />
        for dep in VFFSL(SL, "departments", True):  # generated from line 371, col 9
            write("""            <button id='""")
            _v = VFFSL(SL, "dep", True)["name"]  # "$dep['name']" on line 372, col 25
            if _v is not None:
                write(_filter(_v, rawExpr="$dep['name']"))  # from line 372, col 25.
            write("""' class='department_button' value=""")
            _v = VFFSL(SL, "dep", True)  # '$dep' on line 372, col 71
            if _v is not None:
                write(_filter(_v, rawExpr="$dep"))  # from line 372, col 71.
            write(""">""")
            _v = VFFSL(SL, "dep", True)["label"]  # "$dep['label']" on line 372, col 76
            if _v is not None:
                write(_filter(_v, rawExpr="$dep['label']"))  # from line 372, col 76.
            write(
                """</button>
            <div id='my-form-"""
            )
            _v = VFFSL(SL, "dep", True)["name"]  # "$dep['name']" on line 373, col 30
            if _v is not None:
                write(_filter(_v, rawExpr="$dep['name']"))  # from line 373, col 30.
            write(
                """' class='my-forms' title='Enter ISBN, Author/Title or Price' data-name="""
            )
            _v = VFFSL(SL, "dep", True)["name"]  # "$dep['name']" on line 373, col 113
            if _v is not None:
                write(_filter(_v, rawExpr="$dep['name']"))  # from line 373, col 113.
            write(""" data-label=""")
            _v = VFFSL(SL, "dep", True)["label"]  # "$dep['label']" on line 373, col 137
            if _v is not None:
                write(_filter(_v, rawExpr="$dep['label']"))  # from line 373, col 137.
            write(""" data-is_inventoried_item=""")
            _v = VFFSL(SL, "dep", True)[
                "isInventoriedItem"
            ]  # "$dep['isInventoriedItem']" on line 373, col 176
            if _v is not None:
                write(
                    _filter(_v, rawExpr="$dep['isInventoriedItem']")
                )  # from line 373, col 176.
            write(""" data-is_taxable=""")
            _v = VFFSL(SL, "dep", True)[
                "isTaxable"
            ]  # "$dep['isTaxable']" on line 373, col 218
            if _v is not None:
                write(
                    _filter(_v, rawExpr="$dep['isTaxable']")
                )  # from line 373, col 218.
            write(
                """>
                <form action='' method='get'>
                    <input class='isbnfield' type='text' name='isbn' />"""
            )
            write(
                """                    <div class="special_order_div" style=\'display: none;\'>
                        <input type=\'checkbox\' class=\'is_special_order_checkbox\' value=\'is_special_order\'><span>This is a special order</span>
                        <div class=\'special_order_data_div\' style=\'display:none\'> for <select class=\'special_order_data_select\'></select></div>
                    </div>

"""
            )
            # replaced by smarter textbox which checks if isbn & then either
            # does ajax or sends to select_item_search page.
            # if $dep['isInventoriedItem']
            #     <input type="button" value="Search" onclick="window.open('/register/select_item_search', '_self');" /><br>
            # end if
            write(
                """               </form>
               <div id='title_list_panel' class='title_list_panel' name='title_list_panel'>
                    <ul id='title_list' class='title_list' name='title_list'></ul>
               </div>  
            </div>
"""
            )
        column_keys = ["department", "booktitle", "isbn", "ourprice"]
        write(
            """        <div id="cart_table_panel">
              <table id=\'cart_table\'>
                <thead></thead>
                <tbody>
"""
        )
        if VFFSL(SL, "session_data", True):  # generated from line 397, col 21
            if VFFSL(SL, "session_data.items", True):  # generated from line 398, col 25
                for item in VFFSL(
                    SL, "session_data.items", True
                ):  # generated from line 399, col 29
                    write(
                        """                                <tr>
"""
                    )
                    for key in VFFSL(
                        SL, "column_keys", True
                    ):  # generated from line 401, col 37
                        write(
                            """                                        <td>
"""
                        )
                        try:  # generated from line 403, col 45
                            write(
                                """                                                """
                            )
                            _v = VFFSL(SL, "item", True)[
                                VFFSL(SL, "key", True)
                            ]  # '$item[$key]' on line 404, col 49
                            if _v is not None:
                                write(
                                    _filter(_v, rawExpr="$item[$key]")
                                )  # from line 404, col 49.
                            write(
                                """
"""
                            )
                        except:  # generated from line 405, col 45
                            pass
                        write(
                            """                                        </td>
"""
                        )
                    write(
                        """                                    <td><input type="button" class="remove_item" value="Drop from Cart" /></td>
                                </tr>
"""
                    )
        write(
            """                </tbody>
            </table>
        </div>
        <button id="void_sale" name="void_sale">Void Entire Sale</button><button id="check_out" name="check_out">Remove Items from Inventory</button>
    </div>
    
    <div id=\'isbn_not_found_error\' class=\'error_dialog\' title=\'Error: ISBN not found\'>
        Check the ISBN again or use the search button to search the inventory by attributes.
    </div>
    
    <div id=\'price_dialog\' class=\'query_dialog\' title=\'Query\'>
        Select price of item:
        <select id=\'price_select\'>
            <option value="" disabled="disabled" selected="selected"></option>
        </select>
    </div>
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

    _mainCheetahMethod_for_CartTemplate2 = "writeBody"


## END CLASS DEFINITION

if not hasattr(CartTemplate2, "_initCheetahAttributes"):
    templateAPIClass = getattr(CartTemplate2, "_CHEETAH_templateClass", Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(CartTemplate2)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://cheetahtemplate.org/

##################################################
## if run from command line:
if __name__ == "__main__":
    from Cheetah.TemplateCmdLineIface import CmdLineIface

    CmdLineIface(templateObj=CartTemplate2()).run()
