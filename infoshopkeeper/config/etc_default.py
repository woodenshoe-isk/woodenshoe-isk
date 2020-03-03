# name, password, etc for the mysql database
# fyi we have two databases, infoshopkeeper and infoshopkeeper2
# infoshopkeeper2 is a copy of infoshopkeeper for testing purposes
dbname = "infoshopkeeper2"
dbhost = "hostname"
dbuser = "username"
dbpass = "password"
db_col_password = b"password"
dbtype = "dbtype"

# config files for the wsgi app
# full pathnames to files. Should be in the config directory of ISK install
cherrypy_config_file = "/path/to/file/cherrypy.conf"
cherrypy_global_config_file = (
    "/path/to/file /cherrypy_global.conf"
)
cherrypy_nonlocal_config_file = (
    "/path/to/file/cherrypy_nonlocal.conf"
)
cherrypy_local_config_file = (
    "/path/to/file/cherrypy_local.conf"
)

# logging preferences
client_side_logging_enabled = True
should_log_SQLObject = True

# Sales tax rate
taxrate = 0.08

# do we use amazon ecs account or try to scrape amazon?
use_amazon_ecs = False
amazon_license_key = "license_key"
amazon_secret_key = "secret_key"
amazon_associate_tag = "associate_key"


# if we're scraping amazon, we need to rotate our User-Agent header value so Amazon doesn't kick us.
user_agents_file = "/Path?to?Install/config/user_agents.txt"

# just a reminder that we could work with a usb cash drawer.
open_cash_drawer = "echo 'DO SOMETHING TO MAKE A DRAWER OPEN HERE'"

# if we're using a label printer
label_printer_name = "Brother_QL-570"

# images are stored in db as url's to amazon or books4u
# once we use an image of a certain isbn and size, we cahche it in this directory tree
should_show_images = True
image_directory_root = "/var/www/isk-production/infoshopkeeper/inventoryserver/images"
image_default_small = "book_75.png"
image_default_small_url = "/images/" + image_default_small

# department categories for cart
departments = [
    {"name": "book", "label": "Book", "isInventoriedItem": True, "isTaxable": True},
    {"name": "music", "label": "Music", "isInventoriedItem": True, "isTaxable": True},
    {"name": "film", "label": "Film", "isInventoriedItem": True, "isTaxable": True},
]

# books in inventroy can have any of several statuses.
# STOCK and SOLD are obvious. NOT FOUND is used in year-end inventory, when a book can't be located.
bookStatus = ("STOCK", "SOLD", "NOT FOUND")

# report classes named in report.py which you want to show up in the inventory server
reports = [
    "SalesReport",
    "BestSellersReport",
    "ThingsForNewItemsShelfReport",
    "PossibleMultipleEditionsReport",
    "TransactionReport",
]

# are we using a fake isbn prefix for books or other items that lack isbn or upc
# the range 140-199 for the first three digits is reserved as unallocated
internal_isbn_prefix = '199'

# we don't consign or otherwise sublet our inventory, so not a thing
default_owner = "wooden shoe"

# obviously -- but see the Kind table in db for all kinds
default_kind = "books"
