dbname="infoshopkeeper2"
dbhost="localhost"
dbuser="woodenshoe"
dbpass=""

#pragma variable for wooden shoe specific code
#added 2008-07-26 markos kapes
WOODEN_SHOE=True

#added 2007-02-10 john duda
dbtype="mysql"
title="INFOSHOPKEEPER: Free software with a circled A"


cherrypy_config_file="/home/tech/Developer/infoshopkeeper/cherrypy.conf"
cherrypy_global_config_file="/home/tech/Developer/infoshopkeeper/cherrypy_global.conf"
cherrypy_nonlocal_config_file="/home/tech/Developer/infoshopkeeper/cherrypy_nonlocal.conf"
cherrypy_local_config_file="/home/tech/Developer/infoshopkeeper/cherrypy_local.conf"

taxrate=0.08

amazon_license_key="AKIAJZ33OWZPPGD5MCGA"
amazon_secret_key="c7YtCZWQUxv2jHoDd0xdH7pKx5hnLuvmF0YLQlpw"

open_cash_drawer="echo 'DO SOMETHING TO MAKE A DRAWER OPEN HERE'"

# e.g. "/home/infoshopkeeper/infoshopkeeper/opendrawer /dev/usb/hid/hiddev0"
# in the case of red emma's, you probably need to do something else, but if
# you have an apg54 usb-hid cash drawer, we've got the code your looking for!

# The simple item buttons
# Full Name, Short Label, Price, {Color, Page}
simple_items= ()
""" ("In House Coffee","In House Coffee",1.43,{"color":"#3333ff","taxable":False}),
    ("Small Coffee","Sm Coffee",1.14,{"color":"#3333ff","page":"things"}),
    ("Medium Coffee","Me Coffee",1.52,{"color":"#3333ff","page":"things"}),
    ("Large Coffee","Lg Coffee",1.90,{"color":"#3333ff"}),
    ("Tea","Tea",1.19,{"color":"#3333ff"}),
    ("Extra Tea Bag","Extra Tea Bag",0.24,{"color":"#3333ff"}),
    ("Yerba Mate","Yerba Mate", 1.90,{"color":"#3333ff"}),
    ("Mexican Hot Chocolate","Hot Choc",1.90,{"color":"#ff3333"}),
    ("Chai","Chai",2.38,{"color":"#ff3333"}),
    ("Single Espresso","Single Espresso",1.43,{"color":"#ff0033"}),
    ("Double Espresso","Double Espresso",1.90,{"color":"#ff0033"}),
    ("Single Macch.","Single Macchiato",1.63,{"color":"#ff0033"}),
    ("Double Macch.","Double Macchiato",2.19,{"color":"#ff0033"}),
    ("Small Capp.","Small Cappucino",2.38,{"color":"#ff0033"}),
    ("Medium Capp.","Medium Cappucino",2.86,{"color":"#ff0033"}),
    )"""

#added 2007-02-10 john duda
# The complex item buttons
# Full Name, Short Label, ClassFactory, {Color, Taxable,Page}
complex_items= (
    ("Periodical","Periodical","edition_button",{"color":"#3333ff","taxable":False}),
    ("Tshirt","tshirt","merchandise_button",{"color":"#3333ff","taxable":False}),
    ("Book","books","inventoried_merchandise_button",{"color":"#3333ff","taxable":False}),
    ("Music","music","inventoried_merchandise_button",{"color":"#3333ff","taxable":False}),
)



#The miscellaneous function buttons 
#Name,ClassFactory,{Color,Page,Type}

misc_functions = (
    ("Add book to inventory","inventory","add",{"color":"#3333ff","page":"inventory","type":"book"} ),
    ("Browse inventory","inventory","browse",{"color":"#3333ff","page":"inventory","type":"book"} ),
    ("Add member","members","add",{"color":"#3333ff","page":"members","type":"book"} ),
    ("Browse members","members","browse",{"color":"#3333ff","page":"members","type":"book"} ),
    ("Search emprunt","emprunts","browse",{"color":"#3333ff","page":"members","type":"book"} ),
    ("Manage consignment","consignment","pay",{"color":"#3333ff","page":"consignment","type":"book"} ),
    ("Pay out cash","cash","giveout",{"color":"#3333ff","page":"accounting","type":"book"} ),
    ("Credit","cash","credit",{"color":"#3333ff","page":"accounting","type":"book"} ),
    ("Report","wizards","makepdf",{"color":"#3333ff","page":"accounting","type":"book"} ),

    
)

#department categories
departments= {
"book":
    {'name':'book', 'label':'Book', 'isInventoriedItem':True, 'isTaxable':True},
'music':
    {'name':'music', 'label':'Music', 'isInventoriedItem':True, 'isTaxable':True},
}
    
bookStatus = ("STOCK", "SOLD") 

#report classes named in report.py which you want to show up in the inventory server
reports=["SalesReport","BestSellersReport", "NewItemReport", "ThingsForNewItemsShelfReport", "PossibleMultipleEditionsReport" ]

#these are expressed as a fraction of "list price", until you tell the
#machine otherwise 

#you need to make the corresponding float column in the database on
#the "book" table(remove the spaces in whatever name you use

multiple_prices = []

#multiple_prices = (
#    ("half off",.5),
#    )

default_owner="wooden shoe"

default_kind="books"

