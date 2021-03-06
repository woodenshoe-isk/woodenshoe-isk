import random
import unittest

#from .ecs import InvalidParameterValue
import isbnlib

from objects.book import Book
from objects.title import Title

from tools import inventory, now

UNIT_TEST = True

# class inventory:
# def __init__(self):
# def lookup_by_isbn(self,number):
# def parseBrowseNodes(bNodes):
# def parseBrowseNodesInner(item):
# def addToInventory(self,title="",status="STOCK",authors=None,publisher="",listprice="",ourprice='',isbn="",categories=[],distributor="",location="",owner="",notes="",quantity=1,known_title=False,types='',kind_name="",extra_prices={}, tag=''):
# def getInventory(self,queryTerms):
class test_inventory(unittest.TestCase):
    def test_lookup_by_isbn10_have_it(self):
        random_item = random.sample(list(Title.select("isbn RLIKE '^[0-9]{13}$'")), 1)[
            0
        ]
        result = inventory.lookup_by_isbn(random_item.isbn)
        self.assertEqual(
            random_item.isbn,
            result["isbn"],
            "inventory.lookup_by_isbn returned wrong isbn for random isbn10 in database",
        )

    def test_lookup_by_isbn10_dont_have(self):
        isbn_we_will_never_have = "0060723467"  # Dick Cheney's autobiography
        result = inventory.lookup_by_isbn(isbn_we_will_never_have)
        print("RESULT IS:", result)
        isbn_we_will_never_have = isbnlib.to_isbn13(isbn_we_will_never_have)
        self.assertEqual(isbn_we_will_never_have, result["isbn"])

    def test_lookup_by_isbn10_is_invalid(self):
        # translation table of checkdigits to wrong ones (digit plus 1)
        tr_table = dict(
            list(
                zip(
                    ["x", "X"] + list(map(str, list(range(9, -1, -1)))),
                    ["0", "0", "x"] + list(map(str, list(range(9, 0, -1)))),
                )
            )
        )
        random_item = random.sample(list(Title.select("isbn RLIKE '^[0-9]{13}$'")), 1)[
            0
        ]
        wrong_isbn = isbnlib.to_isbn10(random_item.isbn)
        wrong_isbn = wrong_isbn[0:9] + tr_table[wrong_isbn[9]]
        with self.assertRaises((isbnlib.NotValidISBNError, isbnlib._exceptions.NotValidISBNError)):
            result = inventory.lookup_by_isbn(wrong_isbn)

    def test_lookup_by_orig_isbn_is_valid(self):
        random_item = random.sample(list(Title.select("isbn RLIKE '^[0-9]{13}$'")), 1)[
            0
        ]
        result = inventory.lookup_by_isbn(random_item.isbn)
        self.assertEqual(
            random_item.isbn,
            result["isbn"],
            "inventory.lookup_by_isbn returned wrong isbn for random isbn in database",
        )

    def test_lookup_by_orig_isbn_has_extra_spaces(self):
        random_item = random.sample(list(Title.select("isbn RLIKE '^[0-9]{13}$'")), 1)[
            0
        ]
        prepared_isbn = (
            random_item.isbn[0:3]
            + " "
            + random_item.isbn[3:8]
            + " "
            + random_item.isbn[8:]
        )
        result = inventory.lookup_by_isbn(prepared_isbn)
        self.assertEqual(
            random_item.isbn,
            result["isbn"],
            "inventory.lookup_by_isbn returned wrong isbn for random isbn in database",
        )

    def test_lookup_by_orig_isbn_has_extra_hyphens(self):
        random_item = random.sample(list(Title.select("isbn RLIKE '^[0-9]{13}$'")), 1)[
            0
        ]
        prepared_isbn = (
            random_item.isbn[0:3]
            + "-"
            + random_item.isbn[3:8]
            + "-"
            + random_item.isbn[8:]
        )
        result = inventory.lookup_by_isbn(prepared_isbn)
        self.assertEqual(
            random_item.isbn,
            result["isbn"],
            "inventory.lookup_by_isbn returned wrong isbn for random isbn in database",
        )

    def test_lookup_by_orig_isbn_is_invalid(self):
        random_item = random.sample(list(Title.select("isbn RLIKE '^[0-9]{13}$'")), 1)[
            0
        ]
        wrong_isbn = random_item.isbn[0:12] + str((int(random_item.isbn[12]) + 1) % 10)
        print(random_item.isbn, wrong_isbn)
        with self.assertRaises((isbnlib.NotValidISBNError, isbnlib._exceptions.NotValidISBNError)):
            inventory.lookup_by_isbn(wrong_isbn)

    def test_lookup_by_isbn_is_reg(self):
        random_item = random.sample(
            list(Title.select("isbn RLIKE 'reg [0-9]{3,5}'")), 1
        )[0]
        result = inventory.lookup_by_isbn(random_item.isbn)
        self.assertEqual(
            random_item.isbn,
            result["isbn"],
            "inventory.lookup_by_isbn returned wrong isbn for random isbn (reg) in database",
        )

    def test_lookup_by_isbn_is_wsr(self):
        random_item = random.sample(
            list(Title.select("isbn RLIKE 'wsr [0-9]{3,5}'")), 1
        )[0]
        result = inventory.lookup_by_isbn(random_item.isbn)
        self.assertEqual(
            random_item.isbn,
            result["isbn"],
            "inventory.lookup_by_isbn returned wrong isbn for random isbn (wsr) in database",
        )

    def test_addToInventory_have_title(self):
        random_item = random.sample(list(Book.selectBy(status="STOCK")), 1)[0]
        fakeargs = dict(
            title=random_item.title.booktitle,
            authors=random_item.title.authors_as_string(),
            publisher=random_item.title.publisher,
            distributor=random_item.distributor,
            owner="woodenshoe",
            listprice=random_item.listprice,
            ourprice=random_item.ourprice,
            isbn=random_item.title.isbn,
            categories=random_item.title.categories_as_string(),
            location=random_item.location.locationName,
            location_id=random_item.locationID,
            quantity=1,
            known_title=random_item.title,
            types=random_item.title.type,
            kind_name=random_item.title.kind.kindName,
        )
        print(fakeargs)
        inventory.addToInventory(**fakeargs)
        today = now.Now.now.strftime("%Y-%m-%d")
        confirm = Book.selectBy(titleID=random_item.titleID).filter(
            Book.q.inventoried_when == today
        )
        try:
            self.assertTrue(
                confirm,
                "inventory.addToInventory of title that we have does not add item to inventory",
            )
        finally:
            print(("confirm: ", list(confirm), confirm[-1]))
            confirm[-1].destroySelf()

    def test_addToInventory_dont_have_title(self):
        pass


#     def test_getInventory_title(self):
#         random_item=random.sample(list(Book.selectBy(status='STOCK')), 1)[0]
#         result=inventory.getInventory(title=random_item.title.booktitle).count()
#         assertTrue(result, 'inventory.getInventory does not get books by title')
#     def test_getInventory_status_stock(self):
#         random_item=random.sample(list(Book.selectBy(status='STOCK')), 1)[0]
#         result=inventory.getInventory(status='STOCK').count()
#         assertTrue(result, 'inventory.getInventory does not get books by status \'STOCK\'')
#     def test_getInventory_author(self):
#         random_item=random.sample(list(Book.selectBy(status='STOCK')), 1)[0]
#         result=inventory.getInventory(author=random_item.title.author[0].authorName).count()
#         assertTrue(result, 'inventory.getInventory does not get books by author')
#     def test_getInventory_publisher(self):
#         random_item=random.sample(list(Book.selectBy(status='STOCK')), 1)[0]
#         result=inventory.getInventory(publisher=random_item.title.publisher).count()
#         assertTrue(result, 'inventory.getInventory does not get books by publisher')
#     def test_getInventory_isbn(self):
#         random_item=random.sample(list(Book.selectBy(status='STOCK')), 1)[0]
#         result=inventory.getInventory(publisher=random_item.title.isbn).count()
#         assertTrue(result, 'inventory.getInventory does not get books by isbn')
#     def test_getInventory_category(self):
#         random_item=random.sample(list(Book.selectBy(status='STOCK')), 1)[0]
#         result=inventory.getInventory(category=random_item.title.categorys[0]).count()
#         assertTrue(result, 'inventory.getInventory does not get books by category')
#     def test_getInventory_distributor(self):
#         random_item=random.sample(list(Book.selectBy(status='STOCK')), 1)[0]
#         result=inventory.getInventory(distributor=random_item.distributor).count()
#         assertTrue(result, 'inventory.getInventory does not get books by distributor')
#     def test_getInventory_location(self):
#         random_item=random.sample(list(Book.selectBy(status='STOCK')), 1)[0]
#         result=inventory.getInventory(location=random_item.location).count()
#         assertTrue(result, 'inventory.getInventory does not get books by location')
#     def test_getInventory_owner(self):
#         random_item=random.sample(list(Book.selectBy(status='STOCK')), 1)[0]
#         result=inventory.getInventory(owner=random_item.owner).count()
#         assertTrue(result, 'inventory.getInventory does not get books by owner')
#     def test_getInventory_quantity(self):
#         pass
#     def test_getInventory_types(self):
#         pass
#     def test_getInventory_kind(self):
#         pass
#     def test_getInventory_tag(self):
#         pass
#


"""class Test_AmazonErrorclass Test_NoLicenseKeydef test_versiondef test_setAssociatedef test_getAssociatedef test__checkLocaleSupporteddef test_setLocaledef test_getLocaledef test_setLicensedef test_getLicensedef test_setProxydef test_getProxydef test_getProxiesdef test__contentsOfdef test__getScriptDirclass Test_Bag:def test_unmarshaldef test_buildURLdef test_searchByKeyworddef test_browseBestSellersdef test_searchByASINdef test_searchByUPCdef test_searchByAuthordef test_searchByArtistdef test_searchByActordef test_searchByDirectordef test_searchByManufacturerdef test_searchByListManiadef test_searchSimilardef test_searchByWishlistdef test_searchByPowerdef test_searchByBlended    def test_connect    def test_conn    def test_now    def test_regexp    class Test_SQLiteCustomConnection        def test___init__        def test_registerFunctions    def test_connect    def test_conndef test___buildPlugins    def test_collapse    def test_mergePlugins    def test_unionPluginsclass Test_Bag :    def test___repr__def test_rawObjectdef test_rawIteratorclass Test_listIteratordef test_pagedWrapperclass Test_pagedIterator:    def test___init__    def test___len__    def test___iter__    def test___next__    def test___getitem__class Test_AWSExceptionclass Test_NoLicenseKeyclass Test_NoSecretAccessKeyclass Test_NoAssociateTagclass Test_BadLocaleclass Test_BadOptionclass Test_ExactParameterRequirementclass Test_ExceededMaximumParameterValuesclass Test_InsufficientParameterValuesclass Test_InternalErrorclass Test_InvalidEnumeratedParameterclass Test_InvalidISO8601Timeclass Test_InvalidOperationForMarketplaceclass Test_InvalidOperationParameterclass Test_InvalidParameterCombinationclass Test_InvalidParameterValueclass Test_InvalidResponseGroupclass Test_InvalidServiceParameterclass Test_InvalidSubscriptionIdclass Test_InvalidXSLTAddressclass Test_MaximumParameterRequirementclass Test_MinimumParameterRequirementclass Test_MissingOperationParameterclass Test_MissingParameterCombinationclass Test_MissingParametersclass Test_MissingParameterValueCombinationclass Test_MissingServiceParameterclass Test_ParameterOutOfRangeclass Test_ParameterRepeatedInRequestclass Test_RestrictedParameterValueCombinationclass Test_XSLTTransformationErrordef test_setLocaledef test_getLocaledef test_setLicenseKeydef test_getLicenseKeydef test_setSecretAccessKeydef test_getSecretAccessKeydef test_setAssociateTagdef test_getAssociateTagdef test_getVersiondef test_setOptionsdef test_getOptionsdef test_buildSignaturedef test_buildQuerydef test_buildRequestdef test_buildException    class_name = error.childNodes[0].firstChild.data[4:def test_querydef test_unmarshaldef test_ItemLookupdef test_XMLItemLookupdef test_ItemSearchdef test_XMLItemSearchdef test_SimilarityLookupdef test_XMLSimilarityLookupdef test_ListLookupdef test_XMLListLookupdef test_ListSearchdef test_XMLListSearchdef test_CartCreatedef test_XMLCartCreatedef test_CartAdddef test_XMLCartAdddef test_CartGetdef test_XMLCartGetdef test_CartModifydef test_XMLCartModifydef test_CartCleardef test_XMLCartCleardef test___fromListToItemsdef test___cartOperationdef test_SellerLookupdef test_XMLSellerLookupdef test_SellerListingLookupdef test_XMLSellerListingLookupdef test_SellerListingSearchdef test_XMLSellerListingSearchdef test_CustomerContentSearchdef test_XMLCustomerContentSearchdef test_CustomerContentLookupdef test_XMLCustomerContentLookupdef test_BrowseNodeLookupdef test_XMLBrowseNodeLookupdef test_Helpdef test_XMLHelpdef test_TransactionLookupdef test_XMLTransactionLookupdef test_format_currencydef test__process_isbn                def test_parseBrowseNodes                    def test_parseBrowseNodesInnerdef test_search_by_keyword    def test_database_gen    def test_amazon_gen        def test_process_data            def test_parseBrowseNodes                def test_parseBrowseNodesInnerdef test_searchInventorydef test_getInventorydef test_updateItemclass Test_ISBNInvalidclass Test_ISBNNotConvertibledef test_isbn_stripdef test_convertdef test_isValiddef test_checkdef test_checkI10def test_isI10def test_checkI13def test_isI13def test_toI10def test_toI13def test_urlclass Test_Nowclass Test_Emptyclass Test_PersistentQueue:    def test___init__    def test__init_index        def test__load_cache    def test__sync_index    def test__split    def test__join    def test__sync    def test___len__    def test__put    def test__get    def test__qsize    def test_qsize    def test_task_done    def test_join    def test_sync    def test_empty    def test_full    def test_put    def test_put_nowait    def test_get    def test_get_nowait    def test_close    class Test_MyThread        def test___init__        def test_rundef test_run_sql_select"""
