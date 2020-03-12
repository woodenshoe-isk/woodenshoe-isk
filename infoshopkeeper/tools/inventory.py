from time import time, asctime, localtime, sleep
import types, string, random, traceback

from . import ecs
from config.config import configuration

from objects.title import Title
from objects.book import Book
from objects.author import Author
from objects.category import Category
from objects.images import Images
from objects.kind import Kind
from objects.location import Location
from objects.title import Title
from objects.title_special_order import TitleSpecialOrder

import isbnlib

from amzsear import AmzSear

import sys
import re

from urllib.error import HTTPError
import requests
from bs4 import BeautifulSoup

from sqlobject.sqlbuilder import Field, RLIKE, AND, OR, LEFTJOINOn
from MySQLdb import escape_string

use_amazon_ecs = configuration.get("use_amazon_ecs")
amazon_license_key = configuration.get("amazon_license_key")
amazon_secret_key = configuration.get("amazon_secret_key")
amazon_associate_tag = configuration.get("amazon_associate_tag")
default_kind = configuration.get("default_kind")
internal_isbn_prefix = configuration.get("internal_isbn_prefix")

# so we're monkeypatching isbnlib to also accept ourinternal isbns
isbn13_regex_template = '%s{1}(?:-?\d){10,16}|%s{1}[- 0-9]{10,16}'
isbn_prefixes = ['97[89]',]
if internal_isbn_prefix:
    isbn_prefixes.append(internal_isbn_prefix)
isbn13_regex = [isbn13_regex_template % (x, x) for x in isbn_prefixes]
isbn13_regex = '|'.join(isbn13_regex)
isbn13_regex = re.compile(isbn13_regex, re.I)

try:
    user_agent_filename = configuration.get("user_agents_file")
    with open(user_agent_filename, "r") as ua:
        user_agents = ua.read().split()
except Exception as e:
    print(e, file=sys.stderr)
    user_agents = []


def _process_isbn(isbn):
    # only strip quotes if wsr, reg, or consignment number, or none
    if re.match("^wsr|^reg|^\d{2,4}-\d{1,4}$|n/a|none", isbn, re.I):
        isbn = re.sub("['\"]", "", isbn)
        price = 0.00
    # strip quotes, dashes and whitespace. convert isbn10 to isbn13.
    # split isbn and price if it's an extended isbn
    else:
        isbn = re.sub("[\s'\"\-]", "", isbn)
        price = 0.00
        # note the checking for the first character of ean5 extension
        # if it's 5, it means price is in us dollars 0-99.99
        # otherwise, we need to do price ourself.
        if len(isbn) == 18:
            if isbn[-5] == "5":
                price = float(isbn[-4:]) / 100
            isbn = isbn[:-5]
        if len(isbn) == 10:
            if isbnlib.is_isbn10(isbn):
                isbn = isbnlib.to_isbn13(isbn)
            else:
                raise isbnlib.NotValidISBNError(isbn)
        print("isbn13_match", re.match(isbn13_regex, isbn))
        if re.match(isbn13_regex, isbn):
            #can't use isbnlib.is_isnb13 because of internal isbns
            if isbnlib.check_digit13(isbn[0:12]) != isbn[12]:
                raise isbnlib.NotValidISBNError(isbn)
        else:
            raise isbnlib.NotValidISBNError
    return isbn, price


def lookup_by_isbn(number, forceUpdate=False):
    isbn, price = _process_isbn(number)
    print("Looking up isbn", isbn, "with price", price)

    # if length of isbn>0 and isn't "n/a" or "none"
    if len(isbn) > 0 and not re.match("^n(\s|/){0,1}a|none", isbn, re.I):
        # first we check our database
        titles = Title.select(Title.q.isbn == isbn)
        ##print titles #debug
        known_title = False
        the_titles = list(titles)
        if (len(the_titles) > 0) and (not forceUpdate):
            ##print "in titles"
            known_title = the_titles[0]
            ProductName = the_titles[0].booktitle.format()
            authors = []
            if len(the_titles[0].author) > 0:
                authors = [x.authorName.format() for x in the_titles[0].author]
            authors_as_string = ", ".join(authors)
            categories = []
            if len(the_titles[0].categorys) > 0:
                ##print len(the_titles[0].categorys)
                ##print the_titles[0].categorys
                categories = [x.categoryName.format() for x in the_titles[0].categorys]
            categories_as_string = ", ".join(categories)
            if price == 0:
                if len(the_titles[0].books) > 0:
                    ListPrice = max([x.listprice for x in the_titles[0].books])
                else:
                    ListPrice = 0
            else:
                ListPrice = price
            Manufacturer = the_titles[0].publisher.format()
            Format = the_titles[0].type.format()
            Kind = the_titles[0].kind.kindName
            orig_isbn = the_titles[0].origIsbn.format()
            #            if the_titles[0].images:
            #                 large_url = the_titles[0].images.largeUrl
            #                 med_url = the_titles[0].images.medUrl
            #                 small_url = the_titles[0].images.smallUrl
            #            else:
            #                 large_url = med_url = small_url = ''
            large_url = med_url = small_url = ""

            SpecialOrders = [
                tso.id
                for tso in Title.selectBy(
                    isbn=isbn
                ).throughTo.specialorder_pivots.filter(
                    TitleSpecialOrder.q.orderStatus == "ON ORDER"
                )
            ]
            return {
                "title": ProductName,
                "authors": authors,
                "authors_as_string": authors_as_string,
                "categories_as_string": categories_as_string,
                "list_price": ListPrice,
                "publisher": Manufacturer,
                "isbn": isbn,
                "orig_isbn": orig_isbn,
                "large_url": large_url,
                "med_url": med_url,
                "small_url": small_url,
                "format": Format,
                "kind": Kind,
                "known_title": known_title,
                "special_order_pivots": SpecialOrders,
            }
        else:  # we don't have it yet
            # if we're using amazon ecs
            if use_amazon_ecs:
                sleep(1)  # so amazon doesn't get huffy
                ecs.setLicenseKey(amazon_license_key)
                ecs.setSecretAccessKey(amazon_secret_key)
                ecs.setAssociateTag(amazon_associate_tag)

                ##print "about to search", isbn, isbn[0]
                amazonBooks = []

                idType = ""
                if len(isbn) == 12:
                    idType = "UPC"
                elif len(isbn) == 13:
                    # if we are using an internal isbn
                    if isbn.startswith(internal_isbn_prefix):
                        return []
                    # otherwise search on amazon.
                    elif isbn.startswith("978") or isbn.startswith("979"):
                        idType = "ISBN"
                    else:
                        idType = "EAN"
                try:
                    print("searching amazon for ", isbn, idType, file=sys.stderr)
                    amazonProds = AmzSear(isbn)
                    print(amazonProds, file=sys.stderr)
                except (ecs.InvalidParameterValue, HTTPError):
                    pass
                if amazonProds:
                    print(amazonProds, file=sys.stderr)
                    # inner comprehension tests each prodict for price whose type is in formats
                    # if we find a price which its key is in formats, then we return the coorresponding product
                    format_list = [
                        "Paperback",
                        "Mass Market Paperback",
                        "Hardcover",
                        "Perfect Paperback",
                        "Pamphlet",
                        "Plastic Comb",
                        "Spiral-bound",
                        "Print on Demand (Paperback)",
                        "DVD",
                        "Calendar",
                        "Board book",
                        "Audio Cassette",
                        "Cards",
                        "Audio CD",
                        "Diary",
                        "DVD-ROM",
                        "Library Binding",
                        "music",
                        "Vinyl",
                        "Health and Beauty",
                        "Hardback",
                    ]
                    prods = [
                        x
                        for x in amazonProds.values()
                        if [dum for dum in x["prices"].keys() if dum in format_list]
                    ]

                    for prod1 in prods:
                        print(prod1, file=sys.stderr)
                        price_dict = prod1["prices"]
                        listprice = max(price_dict.values())

                        format = [k for k in format_list if k in price_dict]
                        format = format[0]
                        if not format:
                            continue

                        title = prod1["title"]

                        image_url = prod1["image_url"]

                        authors = [
                            x.replace("by ", "")
                            for x in prod1["subtext"]
                            if x.startswith("by ")
                        ]
                        auth_list = [
                            y.strip()
                            for a in [x.split(", ") for x in authors[0].split(" and ")]
                            for y in a
                        ]
                        # we assume any full name less than five characters is an abbreviation like 'Jr.'
                        # so we add it back to the previous authorname
                        abbrev_list = [i for i, x in enumerate(auth_list) if len(x) < 5]
                        for i in abbrev_list:
                            auth_list[i - 1 : i + 1] = [
                                ", ".join(auth_list[i - 1 : i + 1])
                            ]

                        return {
                            "title": title,
                            "authors": auth_list,
                            "authors_as_string": ",".join(auth_list),
                            "categories_as_string": "",
                            "list_price": listprice,
                            "publisher": "",
                            "isbn": isbn,
                            "orig_isbn": isbn,
                            "large_url": image_url,
                            "med_url": image_url,
                            "small_url": image_url,
                            "format": format,
                            "kind": "books",
                            "known_title": known_title,
                            "special_orders": [],
                        }

                else:
                    traceback.print_exc()
                    print("using isbnlib from ecs", file=sys.stderr)
                    isbnlibbooks = []
                    try:
                        isbnlibbooks = isbnlib.meta(str(isbn))
                    except:
                        pass

                    if isbnlibbooks:
                        return {
                            "title": isbnlibbooks["Title"],
                            "authors": isbnlibbooks["Authors"],
                            "authors_as_string": ",".join(isbnlibbooks["Authors"]),
                            "categories_as_string": None,
                            "list_price": price,
                            "publisher": isbnlibbooks["Publisher"],
                            "isbn": isbn,
                            "orig_isbn": isbn,
                            "large_url": None,
                            "med_url": None,
                            "small_url": None,
                            "format": None,
                            "kind": "books",
                            "known_title": known_title,
                            "special_orders": [],
                        }
                    else:
                        return {}
            else:  # if we're scraping amazon
                print("scraping amazon", file=sys.stderr)
                headers = {
                    "User-Agent": random.sample(user_agents, 1).pop()
                }
                amazon_url_template = "http://www.amazon.com/dp/%s/"
                if len(isbn) == 13:
                    isbn10 = None
                    if isbnlib.is_isbn13(isbn):
                        isbn10 = isbnlib.to_isbn10(isbn)
                    else:
                        return {}
                if isbn10:
                    with requests.Session() as session:
                        try:
                            print("getting amazon")
                            page_response = session.get(
                                amazon_url_template % isbn10,
                                headers=headers,
                                timeout=0.1
                            )
                            print("got response")
                            page_content = BeautifulSoup(page_response.content, "lxml")
                            print("got parsed content")
                            try:
                                booktitle = page_content.select("#productTitle").pop().text
                            except Exception as e:
                                traceback.print_exc()
                                booktitle = ''
                            popover_preload = [
                                a.text
                                for a in page_content.select(
                                    ".author.notFaded .a-popover-preload a.a-link-normal"
                                )
                            ]
                            author_name = [
                                a.text
                                for a in page_content.select(
                                    ".author.notFaded a.a-link-normal"
                                )
                                if a.text not in popover_preload
                            ]
                            contributor_role = page_content.select(".contribution span")
                            try:
                                contributor_role = [
                                    re.findall("\w+", cr.text).pop()
                                    for cr in contributor_role
                                ]
                            except Exception as e:
                                traceback.print_exc()
                                contributor_role = []
                            author_role = zip(author_name, contributor_role)
                            try:
                                listprice = (
                                    page_content.select(".a-text-strike").pop().text
                                )
                            except IndexError as e:
                                print("using bookfinder4u")
                                if "listprice" not in locals():
                                    with requests.Session() as session:
                                        bookfinderurl = "http://www.bookfinder4u.com/IsbnSearch.aspx?isbn='%s'&mode=direct"
                                        url = bookfinderurl % isbn
                                        try:
                                            page_response2 = session.get(
                                                url,
                                                headers=headers,
                                                timeout=0.1
                                            )
                                            page_content2 = BeautifulSoup(
                                                page_response2.content, "lxml"
                                            )
                                        except Exception as e:
                                            traceback.print_exc()
                                            listprice = 0.0
                                        else:
                                            try:
                                                matches = re.search(
                                                    "List\sprice:\s(\w{2,4})\s(\d+(.\d+)?)",
                                                    page_content2.text,
                                                    re.I,
                                                )
                                                if matches:
                                                    listprice = matches.groups()[1]
                                                else:
                                                    listprice = 0.00
                                            except Exception as e:
                                                traceback.print_exc()
                                                listprice = 0.00
                            try:
                                book_edition = (
                                    page_content.select("#bookEdition").pop().text
                                )
                            except Exception as e:
                                traceback.print_exc()
                                book_edition = ""
                            try:
                                matches = re.findall(
                                    "(?<=imageGalleryData'\s:\s\[)\{.*?\}",
                                    page_content.contents[1].text,
                                )
                                image_url_dict = eval(matches[0])
                            except Exception as e:
                                traceback.print_exc()
                                image_url_dict = {"mainUrl": "", "thumbUrl": ""}
                            category_items = page_content.select(".zg_hrsr_ladder a")
                            category_items = [a.text for a in category_items]
                            product_details = page_content.select(
                                "#productDetailsTable"
                            )  # ul:first-of-type")
                            try:
                                product_details1 = product_details.pop().text.splitlines()
                                quit_flag = 0
                                for pd in product_details1:
                                    if pd.endswith("pages"):
                                        format, numpages = pd.split(":")
                                        numpages = numpages.replace(" pages", "").strip()
                                        quit_flag += 1
                                        continue
                                    if pd.startswith("Publisher: "):

                                        matches = re.match(
                                            "Publisher: ([^;^(]*)\s?([^(]*)?\W(.*)\W", pd
                                        ).groups()
                                        publisher = matches[0]
                                        publication_date = matches[2]
                                        quit_flag += 1
                                        continue
                                    if quit_flag == 2:
                                        break
                                else:
                                    publisher = ''
                                    format = ''
                            except Exception as e:
                                traceback.print_exc()
                                publisher = ''
                                format = ''
                            if booktitle:
                                return {
                                    "title": booktitle,
                                    "authors": author_name,
                                    "authors_as_string": ",".join(author_name),
                                    "categories_as_string": ",".join(category_items),
                                    "list_price": listprice,
                                    "publisher": publisher,
                                    "isbn": isbn,
                                    "orig_isbn": isbn,
                                    "large_url": image_url_dict["mainUrl"],
                                    "med_url": image_url_dict["mainUrl"],
                                    "small_url": image_url_dict["thumbUrl"],
                                    "format": format,
                                    "kind": "books",
                                    "known_title": known_title,
                                    "special_orders": [],
                                }
                        except Exception as e:
                            traceback.print_exc()
                            print("using isbnlib from scraper", file=sys.stderr)
                            isbnlibbooks = []
                            try:
                                isbnlibbooks = isbnlib.meta(str(isbn))
                            except:
                                pass

                            if isbnlibbooks:
                                return {
                                    "title": isbnlibbooks["Title"],
                                    "authors": isbnlibbooks["Authors"],
                                    "authors_as_string": ",".join(
                                        isbnlibbooks["Authors"]
                                    ),
                                    "categories_as_string": None,
                                    "list_price": price,
                                    "publisher": isbnlibbooks["Publisher"],
                                    "isbn": isbn,
                                    "orig_isbn": isbn,
                                    "large_url": None,
                                    "med_url": None,
                                    "small_url": None,
                                    "format": None,
                                    "kind": "books",
                                    "known_title": known_title,
                                    "special_orders": [],
                                }
                            else:
                                return {}
                else:
                    if title:
                        return {
                            "title": title,
                            "authors": author_name,
                            "authors_as_string": ",".join(author_name),
                            "categories_as_string": ",".join(category_items),
                            "list_price": listprice,
                            "publisher": publisher,
                            "isbn": isbn,
                            "orig_isbn": isbn,
                            "large_url": image_url_dict["mainUrl"],
                            "med_url": image_url_dict["mainUrl"],
                            "small_url": image_url_dict["thumbUrl"],
                            "format": format,
                            "kind": "books",
                            "known_title": known_title,
                            "special_orders": [],
                        }
                    else:
                        return {}
    else:
        return {}


def search_by_keyword(authorOrTitle=""):
    def database_gen(authorOrTitle=""):
        titles = []

        # start out with the join clauses in the where clause list
        where_clause_list = []
        clause_tables = ["book", "author", "author_title"]
        join_list = [
            LEFTJOINOn("title", "book", "book.title_id=title.id"),
            LEFTJOINOn(None, "author_title", "title.id=author_title.title_id"),
            LEFTJOINOn(None, "author", "author.id=author_title.author_id"),
        ]

        # add filter clauses if they are called for
        where_clause_list.append(
            "(author.author_name RLIKE '%s' OR title.booktitle RLIKE '%s')"
            % (authorOrTitle.strip(), authorOrTitle.strip())
        )
        # AND all where clauses together
        where_clause = AND(where_clause_list)
        titles = []

        # do search.
        titles = Title.select(
            where_clause, join=join_list, clauseTables=clause_tables, distinct=True
        )
        for t1 in titles:
            yield {
                "title": t1.booktitle,
                "authors": t1.author,
                "authors_as_string": t1.authors_as_string(),
                "categories_as_string": t1.categories_as_string(),
                "list_price": t1.highest_price_book().ourprice,
                "publisher": t1.publisher,
                "isbn": t1.isbn,
                "format": t1.type,
                "kind": t1.kind.kindName,
                "known_title": t1,
            }

    def amazon_gen(authorOrTitle=""):
        sleep(1)  # so amazon doesn't get huffy
        ecs.setLicenseKey(amazon_license_key)
        ecs.setSecretAccessKey(amazon_secret_key)
        ecs.setAssociateTag(amazon_associate_tag)

        iter1 = ecs.ItemSearch(
            Keywords="python",
            SearchIndex="Books",
            ResponseGroup="ItemAttributes,BrowseNodes",
        )
        # iter1=xrange(0,20)
        def process_data(data):
            result = {}
            authors = []
            categories = []

            for x in ["Author", "Creator", "Artist", "Director"]:
                if hasattr(data, x):
                    if isinstance(getattr(data, x), type([])):
                        authors.extend(getattr(data, x))
                    else:
                        authors.append(getattr(data, x))
            authors_as_string = ", ".join(authors)

            categories_as_string = ""

            # a bit more complicated of a tree walk than it needs be.
            # set up to still have the option of category strings like "history -- us"
            # switched to sets to quickly remove redundancies.
            def parseBrowseNodes(bNodes):
                def parseBrowseNodesInner(item):
                    bn = set()
                    if hasattr(item, "Name"):
                        bn.add(item.Name)
                    if hasattr(item, "Ancestors"):
                        ##print "hasansc"
                        for i in item.Ancestors:
                            bn.update(parseBrowseNodesInner(i))
                    if hasattr(item, "Children"):
                        for i in item.Children:
                            bn.update(parseBrowseNodesInner(i))
                            ##print "bn ", bn

                    if not (hasattr(item, "Ancestors") or hasattr(item, "Children")):
                        if hasattr(item, "Name"):
                            return set([item.Name])
                        else:
                            return set()
                    return bn

                nodeslist = [parseBrowseNodesInner(i) for i in bNodes]
                nodes = set()
                for n in nodeslist:
                    nodes = nodes.union(n)
                return nodes

            categories = parseBrowseNodes(data.BrowseNodes)
            categories_as_string = ", ".join(categories)

            ProductName = ""
            if hasattr(data, "Title"):
                ProductName = data.Title

            Manufacturer = ""
            if hasattr(data, "Manufacturer"):
                Manufacturer = data.Manufacturer

            ListPrice = ""
            if hasattr(data, "ListPrice"):
                ListPrice = data.ListPrice.FormattedPrice.replace("$", "")

            Format = ""
            if hasattr(data, "Binding"):
                Format = data.Binding

            ISBN = ""

            if hasattr(data, "ISBN"):
                ISBN = data.ISBN
            elif hasattr(data, "EAN"):
                ISBN = data.EAN

            Kind = ""
            if data.ProductGroup == "Books":
                Kind = "books"
            elif data.ProductGroup == "Music":
                Kind = "music"
            elif data.ProductGroup in ("DVD", "Video"):
                Kind = "film"

            return {
                "title": ProductName,
                "authors": authors,
                "authors_as_string": authors_as_string,
                "categories_as_string": categories_as_string,
                "list_price": ListPrice,
                "publisher": Manufacturer,
                "isbn": ISBN,
                "format": Format,
                "kind": Kind,
                "known_title": None,
            }

        return (
            process_data(a)
            for a in ecs.ItemSearch(
                Keywords=authorOrTitle,
                SearchIndex="Books",
                ResponseGroup="ItemAttributes,BrowseNodes",
            )
        )

    print("at ", authorOrTitle, file=sys.stderr)
    iter_array = [database_gen]
    # test if internet is up
    try:
        urllib.request.urlopen("http://google.com", timeout=1)
    except:
        pass
    else:
        iter_array.append(amazon_gen)

    print("iterarray ", iter_array, file=sys.stderr)
    for iter1 in iter_array:
        try:
            iter1 = iter1(authorOrTitle)
        except IOError as err:
            print(err)
            yield
        except Exception as err:
            print(err)
            yield
        else:
            print(iter1)
            for element in iter1:
                try:
                    yield element
                except IOError as err:
                    print(err)
                    yield


def addToInventory(
    title="",
    status="STOCK",
    authors=None,
    publisher="",
    listprice="",
    ourprice="",
    isbn="",
    orig_isbn="",
    categories=[],
    distributor="",
    location="",
    location_id="",
    large_url="",
    med_url="",
    small_url="",
    owner="",
    notes="",
    quantity=1,
    known_title=False,
    types="",
    kind_name="",
    kind=default_kind,
    extra_prices={},
    tag="",
    labels_per_copy=1,
    printlabel=False,
    special_orders=0,
):
    print("GOT to addToInventory", file=sys.stderr)
    if not authors:
        authors = []
    if known_title:
        print("known_title ", known_title, file=sys.stderr)
        if not known_title.booktitle:
            known_title.booktitle = title
        if not known_title.publisher:
            known_title.publisher = publisher
        if not known_title.type:
            known_title.type = types
    elif not (known_title):
        print("unknown title", file=sys.stderr)
        # add a title
        the_kinds = list(Kind.select(Kind.q.kindName == kind))
        kind_id = None
        if the_kinds:
            kind_id = the_kinds[0].id
        print("kind id is", kind_id, file=sys.stderr)

        # print>>sys.stderr, title

        title = title
        publisher = publisher
        # print>>sys.stderr, title, publisher
        known_title = Title(
            isbn=isbn,
            origIsbn=orig_isbn,
            booktitle=title,
            publisher=publisher,
            tag=" ",
            type=types,
            kindID=kind_id,
        )
        print(known_title, file=sys.stderr)

        im = Images(
            titleID=known_title.id,
            largeUrl=large_url,
            medUrl=med_url,
            smallUrl=small_url,
        )
        print(im, file=sys.stderr)

        for rawAuthor in authors:
            author = rawAuthor
            theAuthors = Author.selectBy(authorName=author)
            theAuthorsList = list(theAuthors)
            if len(theAuthorsList) == 1:
                known_title.addAuthor(theAuthorsList[0])
            elif len(theAuthorsList) == 0:
                a = Author(authorName=author)
                known_title.addAuthor(a)
            else:
                # We should SQLDataCoherenceLost here
                print(
                    "mmm... looks like you have multiple author of the sama name in your database...",
                    file=sys.stderr,
                )
        for category in categories:
            Category(categoryName=category, title=known_title)
    # the_locations=list(Location.select(Location.q.locationName==location))
    # location_id=1
    # if the_locations:
    #    location_id = the_locations[0].id
    if not ourprice:
        ourprice = listprice
    print("about to enter book loop", file=sys.stderr)
    print("location is", location, file=sys.stderr)
    print("location_id is", location_id, file=sys.stderr)
    for i in range(int(quantity)):
        print("book loop", file=sys.stderr)
        b = Book(
            title=known_title,
            status=status,
            distributor=distributor,
            listprice=listprice,
            ourprice=ourprice,
            location=int(location_id),
            owner=owner,
            notes=notes,
            consignmentStatus="",
        )



def searchInventory(sortby="booktitle", out_of_stock=False, **kwargs):
    # start building the filter list
    where_clause_list = []
    print("kwargs are ", kwargs, file=sys.stderr)
    for k in kwargs:
        if type(k) == bytes:
            kwargs[k] = kwargs[k].decode("utf-8")
    to_delete = [k for k in kwargs if kwargs[k] == ""]
    for td in to_delete:
        del kwargs[td]
    print(len(kwargs), file=sys.stderr)

    # clause_tables=['book', 'author', 'author_title', 'category', 'location']
    clause_tables = ["book", "author", "author_title", "location"]
    join_list = [
        LEFTJOINOn("title", "book", "book.title_id=title.id"),
        LEFTJOINOn(None, "author_title", "title.id=author_title.title_id"),
        LEFTJOINOn(None, "author", "author.id=author_title.author_id"),
        LEFTJOINOn(None, Location, Location.q.id == Book.q.locationID),
    ]
    # join_list=[LEFTJOINOn('title', 'book', 'book.title_id=title.id'), LEFTJOINOn(None, 'author_title', 'title.id=author_title.title_id'), LEFTJOINOn(None, 'author', 'author.id=author_title.author_id'), LEFTJOINOn(None, Category, Category.q.titleID==Title.q.id), LEFTJOINOn(None, Location, Location.q.id==Book.q.locationID)]
    if "the_kind" in kwargs:
        where_clause_list.append(Title.q.kindID == kwargs["the_kind"])
    if "the_location" in kwargs and len(the_location) > 1:
        where_clause_list.append(Book.q.locationID == kwargs["the_location"])
    if "title" in kwargs:
        where_clause_list.append(RLIKE(Title.q.booktitle, kwargs["title"].strip()))
    if "publisher" in kwargs:
        where_clause_list.append(RLIKE(Title.q.publisher, kwargs["publisher"].strip()))
    if "tag" in kwargs:
        where_clause_list.append(RLIKE(Title.q.tag, kwargs["tag"].strip()))
    if "isbn" in kwargs:
        isbn, price = _process_isbn(kwargs["isbn"])
        where_clause_list.append(Title.q.isbn == isbn)
    if "formatType" in kwargs:
        where_clause_list.append(Title.q.type == kwargs["formatType"].strip())
    if "owner" in kwargs:
        where_clause_list.append(RLIKE(Book.q.owner, kwargs["owner"].strip()))
    if "distributor" in kwargs:
        where_clause_list.append(
            RLIKE(Book.q.distributor, kwargs["distributor"].strip())
        )
    if "inv_begin_date" in kwargs:
        where_clause_list.append(Book.q.inventoried_when >= kwargs["inv_begin_date"])
    if "inv_end_date" in kwargs:
        where_clause_list.append(Book.q.inventoried_when < kwargs["inv_end_date"])
    if "sold_begin_date" in kwargs:
        where_clause_list.append(Book.q.sold_when >= kwargs["sold_begin_date"])
    if "sold_end_date" in kwargs:
        where_clause_list.append(Book.q.sold_when < kwargs["sold_end_date"])
    if "author" in kwargs:
        where_clause_list.append(RLIKE(Author.q.authorName, kwargs["author"].strip()))
    if "category" in kwargs:
        where_clause_list.append(
            RLIKE(Category.q.categoryName, kwargs["category"].strip())
        )
    if "status" in kwargs:
        where_clause_list.append(Book.q.status == kwargs["status"].strip())
    if "id" in kwargs:
        where_clause_list.append(Title.q.id == kwargs["id"])
    if "authorOrTitle" in kwargs:
        where_clause_list.append(
            OR(
                RLIKE(Author.q.authorName, kwargs["authorOrTitle"].strip()),
                RLIKE(Title.q.booktitle, kwargs["authorOrTitle"].strip()),
            )
        )

    where_clause = AND(*where_clause_list)

    # do search first. Note it currently doesnt let you search for every book in database, unless you use some sort of
    # trick like '1=1' for the where clause string, as the where clause string may not be blank
    titles = []
    if len(kwargs) > 1 or kwargs.setdefault("out_of_stock", False):
        titles = Title.select(
            where_clause,
            join=join_list,
            orderBy=sortby,
            clauseTables=clause_tables,
            distinct=True,
        )
    # filter for stock status
    # GROUPBY in sqlobject is complicated. We could do it but it's not worth it
    if "out_of_stock" in kwargs:
        titles = [t for t in titles if t.copies_in_status("STOCK") == 0]
    # filter on specific numbers in stock
    if "stock_less_than" in kwargs:
        titles = [
            t
            for t in titles
            if t.copies_in_status("STOCK") <= int(kwargs["stock_less_than"])
        ]
    if "stock_more_than" in kwargs:
        titles = [
            t
            for t in titles
            if t.copies_in_status("STOCK") >= int(kwargs["stock_more_than"])
        ]
    # filter by items sold
    if "sold_more_than" in kwargs:
        titles = [
            t
            for t in titles
            if t.copies_in_status("SOLD") >= int(kwargs["sold_more_than"])
        ]
    if "sold_less_than" in kwargs:
        titles = [
            t
            for t in titles
            if t.copies_in_status("SOLD") >= int(kwargs["sold_less_than"])
        ]
    print(titles, file=sys.stderr)
    return titles


def getInventory(queryTerms):
    print(queryTerms, file=sys.stderr)
    keys = list(queryTerms)
    print("keys are ", keys)
    for k in keys:
        if type(queryTerms[k]) == bytes:
            queryTerms[k] = queryTerms[k].decode("utf-8")

    isbnSelect = ""
    kindSelect = ""
    statusSelect = ""
    titleSelect = ""
    authorSelect = ""
    categorySelect = ""
    clauseTables = []

    if "kind" in keys:  # joins suck, avoid if possible
        kind_map = {}
        for k in [(x.kindName, x.id) for x in list(Kind.select())]:
            kind_map[k[0]] = k[1]
        try:
            kind_id = kind_map[queryTerms["kind"]]
            kindSelect = Book.sqlrepr(
                AND(
                    Field("book", "title_id") == Field("title", "id"),
                    Field("title", "kind_id") == kind_id,
                )
            )
        except:
            pass

    if "status" in keys:
        statusSelect = Book.sqlrepr(Field("book", "status") == queryTerms["status"])

    if (
        ("title" in keys)
        or ("authorName" in keys)
        or ("kind" in keys)
        or ("categoryName" in keys)
        or ("isbn" in keys)
    ):
        clauseTables.append("title")
        # we are going to need to do a join

        if "title" in keys:
            titleSelect = Book.sqlrepr(
                AND(
                    Field("book", "title_id") == Field("title", "id"),
                    RLIKE(Field("title", "booktitle"), queryTerms["title"]),
                )
            )

        if "isbn" in keys:
            isbn, price = _process_isbn(queryTerms["isbn"])
            print("isbn and price are ", isbn, price)
            titleSelect = Book.sqlrepr(
                AND(
                    Field("book", "title_id") == Field("title", "id"),
                    Field("title", "isbn") == isbn,
                )
            )

        if "authorName" in keys:
            # authorSelect="""book.title_id = title.id AND author.title_id=title.id AND author.author_name RLIKE %s""" % (Book.sqlrepr(queryTerms["authorName"]))
            authorSelect = Book.sqlrepr(
                AND(
                    Field("book", "title_id") == Field("title", "id"),
                    Field("author", "id") == Field("author_title", "author_id"),
                    Field("title", "id") == Field("author_title", "title_id"),
                    RLIKE(Field("author", "author_name"), queryTerms["authorName"]),
                )
            )
            clauseTables.append("author")
            clauseTables.append("author_title")

        if "categoryName" in keys:
            categorySelect = (
                """book.title_id = title.id AND category.title_id=title.id AND category.category_name RLIKE %s"""
                % (Book.sqlrepr(queryTerms["categoryName"]))
            )
            clauseTables.append("category")
    try:
        books = Book.select(
            " AND ".join(
                [
                    term
                    for term in [
                        statusSelect,
                        titleSelect,
                        authorSelect,
                        kindSelect,
                        categorySelect,
                    ]
                    if term != ""
                ]
            ),
            clauseTables=clauseTables,
            distinct=True,
        )
    except TypeError:
        books = Book.select(
            " AND ".join(
                [
                    term
                    for term in [
                        statusSelect,
                        titleSelect,
                        authorSelect,
                        kindSelect,
                        categorySelect,
                    ]
                    if term != ""
                ]
            ),
            clauseTables=clauseTables,
        )

    results = {}
    i = 1
    for book_for_info in books:
        theTitle = book_for_info.title.booktitle
        authorString = ", ".join([a.authorName for a in book_for_info.title.author])
        categoryString = ", ".join(
            [c.categoryName for c in book_for_info.title.categorys]
        )
        results[i] = (
            theTitle.capitalize(),
            authorString,
            book_for_info.listprice if book_for_info.listprice is not None else "",
            book_for_info.title.publisher
            if book_for_info.title.publisher is not None
            else "",
            book_for_info.status if book_for_info.status is not None else "",
            book_for_info.title.isbn,
            book_for_info.distributor if book_for_info.distributor is not None else "",
            book_for_info.location.locationName
            if book_for_info.location is not None
            else "",
            book_for_info.notes if book_for_info.notes is not None else "",
            book_for_info.id,
            book_for_info.title.kind and book_for_info.title.kind.kindName
            if book_for_info.title.kind is not None
            else "",
            categoryString,
            book_for_info.title.type if book_for_info.title.type is not None else "",
        )
    return results


def updateItem(id):
    title = Title.get(id)
    title_info = lookup_by_isbn(title.orig_isbn, forceUpdate=True)
