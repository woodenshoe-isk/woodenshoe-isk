dbtype="mysql"
dbname="infoshopkeeper"
dbhost="localhost"
dbuser="infoshopkeeper"
dbpass="infoshopkeeper"

cherrypy_config_file="/my/install/of/infoshopkeeper/config/cherrypy.conf"

title="INFOSHOPKEEPER: robot workers of the world unite!"
taxrate=0.05

use_amazon_ecs = False
amazon_license_key="go get one at http://www.amazon.com/gp/aws/registration/registration-form.html/"

# In case you generate sale report as pdf
pdf_opening_program = "/usr/bin/evince"

# Still in case you generate sale report as PDF
# This will be part of the header.
infoshopname="Red emmas ?"
infoshopaddress="800 St-Paul St"

open_cash_drawer="echo 'DO SOMETHING TO MAKE A DRAWER OPEN HERE'"

# e.g. "/home/infoshopkeeper/infoshopkeeper/opendrawer /dev/usb/hid/hiddev0"
# in the case of red emma's, you probably need to do something else, but if
# you have an apg54 usb-hid cash drawer, we've got the code your looking for!

# The simple item buttons
# Full Name, Short Label, Price, {Color, Page}
simple_items= (
    ("In House Coffee", "In House Coffee", 1.43, {"color":"#3333ff","taxable":False}),
    ("Small Coffee", "Sm Coffee", 1.14, {"color":"#3333ff","page":"things"}),
    ("Medium Coffee", "Me Coffee", 1.52, {"color":"#3333ff","page":"things"}),
    ("Large Coffee", "Lg Coffee", 1.90, {"color":"#3333ff"}),
    ("Tea", "Tea", 1.19, {"color":"#3333ff"}),
    ("Extra Tea Bag", "Extra Tea Bag", 0.24, {"color":"#3333ff"}),
    ("Yerba Mate", "Yerba Mate", 1.90, {"color":"#3333ff"}),
    ("Mexican Hot Chocolate", "Hot Choc", 1.90, {"color":"#ff3333"}),
    ("Chai", "Chai", 2.38, {"color":"#ff3333"}),
    ("Single Espresso", "Single Espresso", 1.43, {"color":"#ff0033"}),
    ("Double Espresso", "Double Espresso", 1.90, {"color":"#ff0033"}),
    ("Single Macch.", "Single Macchiato", 1.63, {"color":"#ff0033"}),
    ("Double Macch.", "Double Macchiato", 2.19, {"color":"#ff0033"}),
    ("Small Capp.", "Small Cappucino", 2.38, {"color":"#ff0033"}),
    ("Medium Capp.", "Medium Cappucino", 2.86, {"color":"#ff0033"}),
    )

# The complex item buttons
# Full Name, Short Label, ClassFactory, {Color, Taxable,Page}
complex_items= (
    ("Periodical", "Periodical", "edition_button", {"color":"#3333ff","taxable":False}),
    ("Tshirt", "tshirt", "edition_button", {"color":"#3333ff","taxable":False}),
    ("Book", "book", "inventoried_merchandise_button", {"color":"#3333ff","taxable":False}),
    ("DVD", "dvd", "easyselect_button", {"color":"#3333ff","taxable":False}),
)

#The miscellaneous function buttons
#Name,ClassFactory,{Color,Page,Type}

misc_functions = (
    ("Add member", "members", "add", {"color":"#3333ff","page":"members","type":"book"} ),
    ("Browse members", "members", "browse", {"color":"#3333ff","page":"members","type":"book"} ),
    ("Search emprunt", "emprunts", "browse", {"color":"#3333ff","page":"emprunts","type":"book"} ),
    ("Add book to inventory", "inventory", "add", {"color":"#3333ff","page":"inventory","type":"book"} ),
    ("Browse inventory", "inventory", "browse", {"color":"#3333ff","page":"inventory","type":"book"} ),
    ("Easy select", "wizards", "select", {"color":"#3333ff","page":"wizards","type":"book"} ),
    ("Editions management", "wizards", "editions", {"color":"#3333ff","page":"wizards","type":"book"} ),
    ("Credit button", "cash", "credit", {"color":"#3333ff","page":"Cash","type":"book"} ),
    ("Manage consignment", "consignment", "pay", {"color":"#3333ff","page":"consignment","type":"book"} ),
    ("Pay out cash", "cash", "giveout", {"color":"#3333ff","page":"Cash","type":"book"} ),
)

# these are the possible status of a book
bookStatus = ("STOCK", "BORROWABLE", "ARCHIVE", "STOLEN", "LOST", "RETURNED")
default_kind = "book"
#these are expressed as a fraction of "list price", until you tell the
#machine otherwise

#you need to make the corresponding float column in the database on
#the "book" table(remove the spaces in whatever name you use

multiple_prices = ()

#multiple_prices = (
#    ("half off",.5),
#    )

default_owner="redemmas"

# This is the interface configuration.
# It is simply a two dimensionnal array of tuple,
# the tuple being the name of the procedure to call
# to draw the sizer (see the lasts procedures in
# wxFrame1.py, the make_ ,,, _sizer being put
# afterward), the proportion argument, and if
# wxGROW is set to true. After each columns of the
# GUI, there's once again the proportion and wxGROW
# flags defined for the row.
#
#
# Check out wxFrame1.py => build_GUI for more info

sizer_list = (
    (
            ("saved_sale", 0, 0),
            ("sale", 1, 1), 0, 1
    ),
    (
            ("simple_items_notebook", 1, 1),
            ("complex_items_notebook", 1, 1),
            ("misc_functions_notebook", 1, 1), 1, 1
    ),
    (
            ("messager", 0, 1)
    )
 )

#report classes named in report.py which you want to show up in the inventory server

reports=["SalesReport", "BestSellersReport", "SalesReportByOwner"]
