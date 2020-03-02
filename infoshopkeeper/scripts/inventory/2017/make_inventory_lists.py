#!/usr/bin/env python3

from config.etc import *
from tools import ecs
from config.config import configuration

import time
import isbnlib
import mysql.connector
import sys
import re


def exit_program(cnx):
    if cnx != None:
        cnx.close()

    sys.exit()


def process_good_isbn(isbn, cnx, good_isbns):
    cursor = cnx.cursor()

    select_stmt = """ SELECT b.ourprice, b.wholesale FROM book as b 
                    LEFT JOIN title as t ON b.title_id = t.id WHERE 
                    t.isbn = %(isbn)s ORDER BY inventoried_when DESC """
    cursor.execute(select_stmt, {"isbn": isbn})

    if cursor.with_rows:
        rows = cursor.fetchall()

        if len(rows) == 0:
            del_cursor = cnx.cursor()
            delete_stmt = "DELETE FROM title WHERE isbn = %(isbn)s"
            try:
                del_cursor.execute(delete_stmt, {"isbn": str(isbn)})
            except mysql.connector.errors.DataError:
                print(str(isbn) + "\n")
                sys.exit()
            cnx.commit()
            del_cursor.close()
            if not find_book_on_amazon(isbn, cnx, missing_isbns):
                find_book_on_isbnlib(isbn, cnx, missing_isbns, bad_isbns)
        else:
            row = rows[0]
            good_isbns.write(str(isbn) + "\t" + str(row[0]) + "\t" + str(row[1]) + "\n")

    cursor.close()


def find_book_on_amazon(isbn, cnx, missing_isbns):
    time.sleep(2)

    try:
        amazonbooks = ecs.ItemLookup(
            isbn, IdType="ISBN", SearchIndex="Books", ResponseGroup="ItemAttributes"
        )
    except ecs.InvalidParameterValue:
        return False

    if amazonbooks:
        len_largest = 0
        for book in amazonbooks:
            if hasattr(book, "Title"):
                the_book = book
                break

        book = the_book

        if hasattr(book, "Manufacturer"):
            publisher = book.Manufacturer
        else:
            publisher = ""

        if hasattr(book, "ListPrice"):
            price = book.ListPrice.FormattedPrice.replace("$", "")
        else:
            price = ""

        if hasattr(book, "Binding"):
            binding = book.Binding
        else:
            binding = ""

        if hasattr(book, "Author"):
            author = book.Author
        else:
            author = ""

        missing_isbns.write(
            str(isbn)
            + "\t"
            + str(book.Title)
            + "\t"
            + str(author)
            + "\t"
            + str(price)
            + "\t"
            + str(binding)
            + "\t"
            + str(publisher)
            + "\n"
        )

        return True
    else:
        return False


def find_book_on_isbnlib(isbn, cnx, missing_isbns, bad_isbns):
    try:
        book = isbnlib.meta(str(isbn))

        missing_isbns.write(
            str(isbn)
            + "\t"
            + str(book["Title"])
            + "\t"
            + str(book["Authors"])
            + "\t"
            + ""
            + "\t"
            + ""
            + "\t"
            + str(book["Publisher"])
            + "\n"
        )
    except Exception as e:
        bad_isbns.write(str(isbn) + "\n")


def process_isbn(isbn, cnx, missing_isbns, bad_isbns, good_isbns):
    ecs.setLicenseKey(amazon_license_key)
    ecs.setSecretAccessKey(amazon_secret_key)
    ecs.setAssociateTag(amazon_associate_tag)

    try:
        cursor = cnx.cursor()
    except Exception as e:
        print("Error in process_isbn when attempting to create cursor: " + str(e))
        sys.exit()

    select_stmt = "SELECT * FROM title WHERE isbn = %(isbn)s"
    cursor.execute(select_stmt, {"isbn": isbn})

    if cursor.with_rows:
        rows = cursor.fetchall()

        if len(rows) == 0:
            if not find_book_on_amazon(isbn, cnx, missing_isbns):
                find_book_on_isbnlib(isbn, cnx, missing_isbns, bad_isbns)

        else:
            process_good_isbn(isbn, cnx, good_isbns)

    cursor.close()


def process_title(title, cnx, bad_titles, good_isbns):
    cursor = cnx.cursor()
    select_stmt = "select isbn from title where booktitle=%(title)s"
    cursor.execute(select_stmt, {"title": title})

    if cursor.with_rows:
        rows = cursor.fetchall()

        if len(rows) == 0:
            bad_titles.write(title + "\n")
        else:
            process_good_isbn(rows[0][0], cnx, good_isbns)

    cursor.close()


if len(sys.argv) < 2:
    print("Usage: You must supply the name of the inventory file to check.")
    sys.exit()

try:
    # Set up db connection
    cnx = mysql.connector.connect(
        user=dbuser, password=dbpass, host=dbhost, database=dbname
    )
except Exception as e:
    print("Error connecting to database: " + str(e))
    exit_program(None)

missing_isbns = open("missing_isbns.csv", "w")
bad_isbns = open("bad_isbns.txt", "w")
bad_titles = open("bad_titles.txt", "w")
good_isbns = open("good_isbns.txt", "w")

with open(sys.argv[1]) as f:
    for line in f:
        line = line.strip()
        if re.search(r"^[0-9][0-9]*$", line):
            process_isbn(int(line), cnx, missing_isbns, bad_isbns, good_isbns)
        else:
            process_title(line, cnx, bad_titles, good_isbns)

missing_isbns.close()
bad_isbns.close()
bad_titles.close()
good_isbns.close()
cnx.close()
