dbname="infoshopkeeper2"
dbhost="localhost"
dbuser="woodenshoe"
dbpass="password"
db_col_password='password'
dbtype="mysql"

cherrypy_config_file="/var/www/isk-production/infoshopkeeper/config/cherrypy.conf"
cherrypy_global_config_file="/var/www/isk-production/infoshopkeeper/config/cherrypy_global.conf"
cherrypy_nonlocal_config_file="/var/www/isk-production/infoshopkeeper/config/cherrypy_nonlocal.conf"
cherrypy_local_config_file="/var/www/isk-production/infoshopkeeper/config/cherrypy_local.conf"

client_side_logging_enabled=True
should_log_SQLObject=True

taxrate=0.08

amazon_license_key="AKIAJZ33OWZPPGD5MCGA"
amazon_secret_key="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"
amazon_associate_tag="wwwwoodenshoe-20"

open_cash_drawer="echo 'DO SOMETHING TO MAKE A DRAWER OPEN HERE'"

label_printer_name='Brother_QL-570'

should_show_images = True
image_directory_root = '/var/www/isk-production/infoshopkeeper/inventoryserver/images'
image_default_small = 'book_75.png'
image_default_small_url = '/images/' + image_default_small

#department categories
departments= [
{'name':'book', 'label':'Book', 'isInventoriedItem':True, 'isTaxable':True},
{'name':'music', 'label':'Music', 'isInventoriedItem':True, 'isTaxable':True},
{'name':'film', 'label':'Film', 'isInventoriedItem':True, 'isTaxable':True},
]
    
bookStatus = ("STOCK", "SOLD", "NOT FOUND") 

#report classes named in report.py which you want to show up in the inventory server
reports=["SalesReport", "BestSellersReport", "ThingsForNewItemsShelfReport", "PossibleMultipleEditionsReport", "TransactionReport"]

#these are expressed as a fraction of "list price", until you tell the
#machine otherwise 

#you need to make the corresponding float column in the database on
#the "book" table(remove the spaces in whatever name you use

multiple_prices = []                 # [("fullprice", 1),]

#multiple_prices = (
#    ("half off",.5),
#    )

default_owner="wooden shoe"

default_kind="books"

