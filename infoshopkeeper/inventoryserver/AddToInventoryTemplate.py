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
__CHEETAH_genTime__ = 1510105565.6922865
__CHEETAH_genTimestamp__ = 'Wed Nov  8 01:46:05 2017'
__CHEETAH_src__ = 'AddToInventoryTemplate.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Nov  8 00:51:24 2017'
__CHEETAH_docstring__ = 'Autogenerated by Cheetah: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class AddToInventoryTemplate(Skeleton):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        super(AddToInventoryTemplate, self).__init__(*args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = 'searchList namespaces filter filtersLib errorCatcher'.split()
            for k,v in KWs.items():
                if k in allowedKWs: cheetahKWArgs[k] = v
            self._initCheetahInstance(**cheetahKWArgs)
        

    def headscripts(self, **KWS):



        ## CHEETAH: generated from #def headscripts at line 4, col 1.
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
        
        write('''<script type="text/javascript" src="/javascript/jquery.form.js"></script>
<script type="text/javascript" src="/javascript/jquery.validate.min.js"></script>
<script type="text/javascript">                                         
    var isbnDirty = false;
    jQuery(document).ready(function() {
        //temporarily use an alert to remind people to check
        //the special order box
        alert("Please remember to check the special order box");
            
           //Ajax setup for error handling
//         jQuery.ajaxSetup({"error":function(XMLHttpRequest,textStatus, errorThrown) {   
//                 alert(textStatus + \'\\\\r\\\\r\' + errorThrown
//                     + \'\\\\r\\\\r\' + XMLHttpRequest.responseText);
//         }});
        
        jQuery(\'#add_to_inventory_form\').ajaxStart( function() {
            jQuery(\'input[type=submit]\', this).attr(\'disabled\', \'disabled\');
        });
        
        jQuery(\'#add_to_inventory_form\').ajaxComplete( function() {
            jQuery(\'input[type=submit]\', this).removeAttr(\'disabled\');
        });

        var dlg=jQuery(\'#isbndialog\').dialog({
            autoOpen: false, 
            modal: true,
            open: function(){
                //set default button on open
                jQuery(\'.ui-dialog-buttonset > button\').blur();
                jQuery(\'.ui-dialog-buttonset > button:last\').focus();
            },
            buttons: {
                //\'Not Use ISBN\': function(){
                //    jQuery(\'#isbn\').val( \'N/A\' ).blur();
                //    dlg.dialog(\'close\');
                //    jQuery(\'#printlabel\').attr(\'checked\', true);
                //    return false;
                //},
                \'Generate ISBN\': function(){
                    jQuery.ajax({url: \'/admin/get_next_unused_local_isbn\', 
                                        success: function(data){
                                            jQuery(\'#isbn\').val(data).blur();
                                        },
                                        async: false,
                                    });                
                    dlg.dialog(\'close\');
                    jQuery(\'#printlabel\').attr(\'checked\', true);
                    return false;
                },
                \'Search for ISBN\': function(){
                    window.open(\'/admin/select_item_for_isbn_search\', \'_self\');
                    dlg.dialog(\'close\');
                    return false;
                },
            }
        });

        //give isbn text box cursor focus 
        jQuery(\'#isbn\').focus();

        //make return go to next text box instead of submit
        jQuery(document).on(\'keypress\', \'.textbox\', function(evt) {
                    if (evt.keyCode == 13||evt.chatCode == 13) {
                            /* FOCUS ELEMENT */
                            var inputs = jQuery(this).parents("form").eq(0).find(":input");
                            var idx = inputs.index(this);
 
                            if (idx == inputs.length - 1) {
                                inputs[0].select()
                            } else {
                                inputs[idx + 1].focus(); //  handles submit buttons
                                inputs[idx + 1].select();
                            }   
                            return false;
                    }   
        });
        
        //isbn autofill
        jQuery(\'#isbn\').blur( function() {
            var isbnstring=jQuery(this).val();
            if (isbnstring != null) {
                isbnstring=isbnstring.toLowerCase();
    
                //scrub spaces & hyphens if isbn is candidate \'real isbn\'
                if (isbnstring.length>11) {
                    isbnstring.replace(\'/[\\s-]/g\', \'\');
                }
                
                if ( jQuery( \'#isbn\' ).val().match(/^[0-9]{13}5[0-9]{4}$/) == null ) {
                    jQuery(\'#printlabel\').prop(\'checked\', true);
                } else {
                    jQuery(\'#printlabel\').prop(\'checked\', false);
                }

                //use isdirty to avoid infinite loop
                if (true) {
                    //check database for isbn
                    jQuery.getJSON( \'/admin/search_isbn\', {isbn:isbnstring}, function(data){
                        //if success, fill in all the other fields
                        data=data[0]
                        jQuery.each(data, function(key, value) {
                            if (key == \'publisher\') {
                                jQuery(\'#publisher\').val(value);
                            } else if ( key == \'authors_as_string\') {
                                jQuery(\'#authors\').val(value);
                            } else if ( key == \'orig_isbn\') {
                                jQuery(\'#orig_isbn\').val(value);
                            } else if ( key == \'large_url\') {
                                jQuery(\'#large_url\').val(value);
                            } else if ( key == \'med_url\') {
                                jQuery(\'#med_url\').val(value);
                            } else if ( key == \'small_url\') {
                                jQuery(\'#small_url\').val(value);
                            } else if ( key == \'categories_as_string\') {
                                jQuery(\'#categories\').val(value);
                            } else if ( key == \'title\') {
                                jQuery(\'#title\').val(value);
                            } else if ( key == \'list_price\') {
                                jQuery(\'#listprice\').val(value);
                                jQuery(\'#ourprice\').val(value);
                            } else if (key == \'isbn\') {
                                jQuery(\'#isbn\').val(value);
                            } else if ( key == \'format\') {
                                jQuery(\'#types\').val(value);
                            } else if (key ==  \'kind\') {
                                jQuery(\'#kind\').val(value);
                            } else if ( key == \'known_title\') {
                                jQuery(\'#known_title\').val(value);
                            } else if ( key == \'most_freq_location\' ) {
                                jQuery(\'#location\').val( value );
                            } else if ( key == \'special_order_pivots\' ) {
                                jQuery( \'#special_orders\').val( value );
                            }
                        });
                    });

                    isbnDirty = true;
                }
            }
            return false;
        });
       
        //check if listprice and ourprice are same. If not, check printlabel
        jQuery(\'#listprice, #ourprice\').blur( function() {
                if (jQuery(\'#listprice\').val() != jQuery(\'#ourprice\').val()) {
                       jQuery(\'#printlabel\').prop(\'checked\', true);
                } else {
                       jQuery(\'#printlabel\').prop(\'checked\', false);
                }
       });

        //jQuery to make select isbn button clickable link
        jQuery(\'#select_isbn_button\').click( function(){
            console.log(\'in click handler\');
            window.open(\'/admin/select_item_for_isbn_search\', \'_self\');
        });
        
        //jQuery validate using class \'required\' in input fields
        jQuery(\'#add_to_inventory_form\').validate({
            onfocusout: true,
            onblur: true,
            rules: {
                isbn: {
                    required: function(){
                        //if there is no isbn, ask whether to generate one
                        //async must be false or it goes on asynchronously
                        //(remember the a in ajax). If you don\'t want an isbn,
                        //it still sets it to \'N/A\' so displays don\'t choke.
                        if (jQuery( \'#isbn\' ).val() == \'\') {
                            //dlg.dialog(\'open\');
                            if (dlg.dialog(\'open\')) {
                                return true;
                            } else {
                                return false;
                            }
                        } else {
                            return false;
                        }
                    }
                }
            },
            submitHandler: function(form) {
                try {
                    jQuery(\'#add_to_inventory_form\').ajaxSubmit({
                        url:\'/admin/add_item_to_inventory\', 
                        clearForm:false, 
                        type:\'post\',
                        success:function(){
                            //add to inventory succeeds
                            
                            //print label if we need to
                            copies_multiplier =  jQuery(\'#labels_per_copy\').val();
                            num_copies = jQuery(\'#quantity\').val();
                            
                            if (jQuery(\'#printlabel\').is(\':checked\')) {
                                total_copies = parseInt(copies_multiplier) * parseInt(num_copies);
                                console.log(\'total_copies is \' + total_copies)
                                jQuery.get(\'/admin/print_label\', {\'isbn\': jQuery(\'#isbn\').val(), \'booktitle\':jQuery(\'#title\').val(), \'authorstring\': jQuery(\'#authors\').val(),\'ourprice\':jQuery(\'#ourprice\').val(),\'listprice\':jQuery(\'#listprice\').val(),\'num_copies\': total_copies});
                            }                        
                            
                            //check on special orders
                            console.log(jQuery(\'#special_orders\').val())
                            special_orders=jQuery(\'#special_orders\').val();
                            if (special_orders=="") {
                                special_orders=[];
                            } else {
                                special_orders = special_orders.split(",");
                            }
                            num_special_orders_to_hold = num_copies - Math.max(num_copies - special_orders.length, 0);
                            console.log("so " + special_orders);
                            console.log("numspec " + num_special_orders_to_hold);
                            if (num_special_orders_to_hold > 0 ) {
                               cop_string = num_special_orders_to_hold == 1 ? \'copy\':\'copies\'
                               alert( num_special_orders_to_hold + \' \' + cop_string
                                       + \' of this book have been special ordered.\'
                                       + \'Please put them aside and attach the special order labels.\');
                               special_orders_to_hold=special_orders.slice(0, num_special_orders_to_hold);
                               args={special_orders:JSON.stringify(special_orders_to_hold), status:\'ON HOLD SHELF\'}
                               console.log(args)
                               jQuery.post(\'/specialorder/set_special_order_item_status\', args);
                            }
                                
                            //clear all text fields except price & quantity
                            //set prices & quantity to defaults
                            //leave pulldown menus as they were
                            
                            console.log("got to zeroing form");
                            jQuery(\'#add_to_inventory_form input.textbox\').not(\'#distributor, #known_title, #quantity, #location, #owner, #status, #kind_name, #listprice, #ourprice\').val(\'\');
                            jQuery(\'#printlabel\').removeAttr(\'checked\');
                            jQuery("#quantity").val(1);
                            jQuery("#listprice").val(\'0.00\');
                            jQuery("#ourprice").val(\'0.00\');
                            jQuery("#known_title").val(\'False\');
                            jQuery(\'#isbn\').focus();
                            isbnDirty=false;
                        }
                    });
                } catch(err) {
                    console.log(err);
                } finally {
                    jQuery(\'#isbn\').focus();
                    return false;
                }
            }                 
        });
        
        jQuery(\'#add_to_inventory_form\').bind(\'reset\', function(){
                
                //clear all text fields except price & quantity
                //set prices & quantity to defaults
                //leave pulldown menus as they were
                jQuery(\'#add_to_inventory_form input.textbox\').not(\'#distributor, #quantity, #location, #owner, #status, #kind_name, #listprice, #ourprice\').val(\'\');
                jQuery(\'#printlabel\').removeAttr(\'checked\');
                jQuery("#quantity").val(1);
                jQuery("#listprice").val(\'0.0\');
                jQuery("#ourprice").val(\'0.0\');
                jQuery(\'#isbn\').focus()
                isbnDirty=false;
        });
    });
</script> 
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def pagetitle(self, **KWS):



        ## CHEETAH: generated from #def pagetitle at line 268, col 1.
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
        
        write('''Add item to  inventory
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def body(self, **KWS):



        ## CHEETAH: generated from #def body at line 272, col 1.
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
        
        write('''<h1>Add to Inventory</h1>
<br />
<form class="outerform" id="add_to_inventory_form" method="post" //~style="visibility:hidden; display:none">

<label class="textbox" for="isbn">Item ID (UPC or ISBN)</label> 
<input class="textbox" minlength=\'1\' type="text" id="isbn" name="isbn" value="''')
        _v = VFFSL(SL,"isbn",True) # '$isbn' on line 278, col 79
        if _v is not None: write(_filter(_v, rawExpr='$isbn')) # from line 278, col 79.
        write('''" />
<input type="button" id=\'select_isbn_button\' value=\'Search for ISBN\'><br />

<label class="textbox" for "printlabel"> </label>
<input type="checkbox" id="printlabel" name="printlabel" 
''')
        if VFFSL(SL,"printlabel",True): # generated from line 283, col 1
            write('''    checked=true 
''')
        write('''value="1" />Print 
<select class="inline" id="labels_per_copy" name="labels_per_copy">
''')
        for i in [1, 2, 3, 4]: # generated from line 288, col 1
            write("""    <option value='""")
            _v = VFFSL(SL,"i",True) # '$i' on line 289, col 20
            if _v is not None: write(_filter(_v, rawExpr='$i')) # from line 289, col 20.
            write("""'>""")
            _v = VFFSL(SL,"i",True) # '$i' on line 289, col 24
            if _v is not None: write(_filter(_v, rawExpr='$i')) # from line 289, col 24.
            write('''</option>
''')
        write('''</select> barcode label for each copy of this title<br />

<label class="textbox" for "quantity">Quantity</label>
<input class="textbox required" type="text" id="quantity", name="quantity", value="''')
        _v = VFFSL(SL,"quantity",True) # '$quantity' on line 294, col 84
        if _v is not None: write(_filter(_v, rawExpr='$quantity')) # from line 294, col 84.
        write('''"/><br />

<label class="textbox" for="title">Title</label> 
<input class="textbox required" type="text" id="title" name="title" value="''')
        _v = VFFSL(SL,"title",True) # '$title' on line 297, col 76
        if _v is not None: write(_filter(_v, rawExpr='$title')) # from line 297, col 76.
        write('''" /><br />

<label class="textbox" for="authors">Author</label> 
<input class="textbox required" type="text" name="authors" id="authors" value="''')
        _v = VFFSL(SL,"authors",True) # '$authors' on line 300, col 80
        if _v is not None: write(_filter(_v, rawExpr='$authors')) # from line 300, col 80.
        write('''" /><br />

<label class="textbox" for="listprice">List Price</label>
<input class="textbox required" type="text" name="listprice" id="listprice" value="''')
        _v = VFFSL(SL,"listprice",True) # '$listprice' on line 303, col 84
        if _v is not None: write(_filter(_v, rawExpr='$listprice')) # from line 303, col 84.
        write('''" /><br />

<label class="textbox" for="ourprice">Our Price</label>
<input class="textbox" type="text" name="ourprice" id="ourprice" value="''')
        _v = VFFSL(SL,"ourprice",True) # '$ourprice' on line 306, col 73
        if _v is not None: write(_filter(_v, rawExpr='$ourprice')) # from line 306, col 73.
        write('''" /><br />

<label class="textbox" for="publisher">Publisher</label> 
<input class="textbox required" type="text" name="publisher" id="publisher" value="''')
        _v = VFFSL(SL,"publisher",True) # '$publisher' on line 309, col 84
        if _v is not None: write(_filter(_v, rawExpr='$publisher')) # from line 309, col 84.
        write('''" /><br />

<label class="textbox" for="categories">Keyword</label> 
<input class="textbox required" type="text" name="categories" id="categories" value="''')
        _v = VFFSL(SL,"categories",True) # '$categories' on line 312, col 86
        if _v is not None: write(_filter(_v, rawExpr='$categories')) # from line 312, col 86.
        write('''" /><br />

<label class="textbox" for="distributor">Distributor</label> 
<select class="textbox required" id="distributor"  name="distributor">
''')
        for d in VFFSL(SL,"distributors",True): # generated from line 316, col 1
            write("""<option value='""")
            _v = VFFSL(SL,"d",True) # '$d' on line 317, col 16
            if _v is not None: write(_filter(_v, rawExpr='$d')) # from line 317, col 16.
            write("""' 
""")
            if "%s" %(VFFSL(SL,"d",True))==VFFSL(SL,"distributor",True): # generated from line 318, col 1
                write('''selected="true" 
''')
            write('''>''')
            _v = VFFSL(SL,"d",True) # '$d' on line 321, col 2
            if _v is not None: write(_filter(_v, rawExpr='$d')) # from line 321, col 2.
            write('''</option>
''')
        write('''</select><br />

<label class="textbox" for="location">Location</label> 
<select class="textbox required" id="location" name="location_id">
<option value=\'\'></option>
''')
        i = 0
        for loc in VFFSL(SL,"locations",True): # generated from line 329, col 1
            write("""<option value='""")
            _v = VFFSL(SL,"loc.id",True) # '$loc.id' on line 330, col 16
            if _v is not None: write(_filter(_v, rawExpr='$loc.id')) # from line 330, col 16.
            write("""' 
""")
            if "%s" %(VFFSL(SL,"loc.id",True))==VFFSL(SL,"location",True): # generated from line 331, col 1
                write('''selected="true" 
''')
            write('''>''')
            _v = VFFSL(SL,"loc.locationName",True) # '$loc.locationName' on line 334, col 2
            if _v is not None: write(_filter(_v, rawExpr='$loc.locationName')) # from line 334, col 2.
            write('''</option>
''')
            i = VFFSL(SL,"i",True)+1
        write('''</select><br />

<label class="textbox" for="owner">Owner</label> 
<input class="textbox" type="text" name="owner" id="owner" value="''')
        _v = VFFSL(SL,"owner",True) # '$owner' on line 340, col 67
        if _v is not None: write(_filter(_v, rawExpr='$owner')) # from line 340, col 67.
        write('''" /><br />

<label class="textbox" for="tag">Tag</label> 
<input class="textbox" type="text" id="tag" name="tag" value="''')
        _v = VFFSL(SL,"tag",True) # '$tag' on line 343, col 63
        if _v is not None: write(_filter(_v, rawExpr='$tag')) # from line 343, col 63.
        write('''" /><br />

<label class="textbox" for="kind">Kind</label> 
<select class="textbox required" id="kind" name="kind">
''')
        for k in VFFSL(SL,"kinds",True): # generated from line 347, col 1
            write("""<option value='""")
            _v = VFFSL(SL,"k.kindName",True) # '$k.kindName' on line 348, col 16
            if _v is not None: write(_filter(_v, rawExpr='$k.kindName')) # from line 348, col 16.
            write("""' 
""")
            if "%s" %(VFFSL(SL,"k.id",True))==VFFSL(SL,"kind",True): # generated from line 349, col 1
                write('''selected="true" 
''')
            write('''>''')
            _v = VFFSL(SL,"k.kindName",True) # '$k.kindName' on line 352, col 2
            if _v is not None: write(_filter(_v, rawExpr='$k.kindName')) # from line 352, col 2.
            write('''</option>
''')
        write('''</select><br />

<label class="textbox" for="type">Format</label> 
<select class="textbox required" id="types" name="types">
''')
        for f in VFFSL(SL,"formats",True): # generated from line 358, col 1
            write("""<option value='""")
            _v = VFFSL(SL,"f",True) # '$f' on line 359, col 16
            if _v is not None: write(_filter(_v, rawExpr='$f')) # from line 359, col 16.
            write("""' 
""")
            if "%s" %(VFFSL(SL,"f",True))==VFFSL(SL,"format",True): # generated from line 360, col 1
                write('''selected="true" 
''')
            write('''>''')
            _v = VFFSL(SL,"f",True) # '$f' on line 363, col 2
            if _v is not None: write(_filter(_v, rawExpr='$f')) # from line 363, col 2.
            write('''</option>
''')
        write("""</select><br />

<input class='textbox' type='hidden' id='known_title' name='known_title' value='""")
        _v = VFFSL(SL,"known_title",True) # '$known_title' on line 367, col 81
        if _v is not None: write(_filter(_v, rawExpr='$known_title')) # from line 367, col 81.
        write("""'/>
<input class='textbox' type='hidden' id='special_orders' name='special_orders'/>
<input class='textbox' type='hidden' id='orig_isbn' name='orig_isbn' value='""")
        _v = VFFSL(SL,"orig_isbn",True) # '$orig_isbn' on line 369, col 77
        if _v is not None: write(_filter(_v, rawExpr='$orig_isbn')) # from line 369, col 77.
        write("""'/>
<input class='textbox' type='hidden' id='large_url' name='large_url' value='""")
        _v = VFFSL(SL,"large_url",True) # '$large_url' on line 370, col 77
        if _v is not None: write(_filter(_v, rawExpr='$large_url')) # from line 370, col 77.
        write("""'/>
<input class='textbox' type='hidden' id='med_url' name='med_url' value='""")
        _v = VFFSL(SL,"med_url",True) # '$med_url' on line 371, col 73
        if _v is not None: write(_filter(_v, rawExpr='$med_url')) # from line 371, col 73.
        write("""'/>
<input class='textbox' type='hidden' id='small_url' name='small_url' value='""")
        _v = VFFSL(SL,"small_url",True) # '$small_url' on line 372, col 77
        if _v is not None: write(_filter(_v, rawExpr='$small_url')) # from line 372, col 77.
        write('''\'/>

<div class="button_panel"><input class="submit" type="submit" action=\'/admin/add_item_to_inventory\' value=\'Add to Inventory\'>
<br />
<input class=\'reset\' type=\'reset\' value=\'Cancel\'>
<br /></div>
</form>
<div id=\'isbndialog\' class=\'isbndialog\' title=\'Alert!\'>
You did not enter an ISBN. If you don\'t see an ISBN, check inside the book, it may still have one.<br /><br />
If the book really doesn\'t have an ISBN, the system can generate one for you (You really checked first though, right?).<br /> <br />
What would you like to do?
</div>
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

    _mainCheetahMethod_for_AddToInventoryTemplate= 'writeBody'

## END CLASS DEFINITION

if not hasattr(AddToInventoryTemplate, '_initCheetahAttributes'):
    templateAPIClass = getattr(AddToInventoryTemplate, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(AddToInventoryTemplate)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://cheetahtemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=AddToInventoryTemplate()).run()


