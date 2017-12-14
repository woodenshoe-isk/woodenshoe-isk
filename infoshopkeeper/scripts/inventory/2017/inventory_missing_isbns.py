#!/usr/bin/env python3

# This script is used to inventory the isbns located in the "missing_isbns.csv" file
# into the database. 

from config.etc import *
from datetime import datetime

import mysql.connector
import sys
import re

def get_title_id(isbn, cnx):
  cursor = cnx.cursor()

  select_stmt = "SELECT id FROM title WHERE isbn = %(isbn)s"
  cursor.execute(select_stmt, { 'isbn': isbn })

  if cursor.with_rows:
    rows = cursor.fetchall()

    if (len(rows) == 0):
      return_value = -1
    else:
      return_value = rows[0][0]

  cursor.close()

  print("SELECT id FROM title WHERE isbn = " + str(isbn) + "\n")
  print("return value " + str(return_value))

  return return_value

def get_author_id(author, title_id, cnx):
  cursor = cnx.cursor()

  select_stmt = "SELECT id FROM author WHERE author_name = %(author)s"
  cursor.execute(select_stmt, { 'author': author, 'title_id': title_id })

  if cursor.with_rows:
    rows = cursor.fetchall()

    if (len(rows) == 0):
      return_value = -1
    else:
      return_value = rows[0][0]

  cursor.close()
  return return_value

def insert_author(author, title_id, cnx):
  cursor = cnx.cursor()

  author_id = get_author_id(author, title_id, cnx)

  if author_id == -1:
    insert_stmt = "INSERT INTO author (author_name, title_id) VALUES (%(author)s, %(title_id)s)"
    cursor.execute(insert_stmt, { 'author': author, 'title_id': title_id })
    cnx.commit()
    author_id = get_author_id(author, title_id, cnx)
      
  cursor.close()
  return author_id

def insert_title(isbn, title, price, binding, publisher, cnx):
  cursor = cnx.cursor()
  
  title_id = get_title_id(isbn, cnx)

  if title_id == -1:
    insert_stmt = """ INSERT INTO title (isbn, booktitle, publisher, 
                      kind_id, type, orig_isbn) VALUES (%(isbn)s, %(title)s, 
                      %(publisher)s, %(kind)s, %(binding)s, %(orig_isbn)s) """  

    cursor.execute(insert_stmt, 
                   { 
                      'isbn': isbn, 
                      'title': title,
                      'publisher': publisher,
                      'kind': 1,
                      'binding': "Unknown Binding",
                      'orig_isbn': isbn
                   })

    cnx.commit()

    title_id = get_title_id(isbn, cnx)

  cursor.close()
  
  print("title id " + str(title_id) + "\n")
  return title_id


def author_title_exists(author_id, title_id, cnx):
  cursor = cnx.cursor()

  select_stmt = "SELECT id FROM author_title WHERE author_id = %(author_id)s and title_id=%(title_id)s"
  cursor.execute(select_stmt, { 'author_id': author_id, 'title_id': title_id })

  if cursor.with_rows:
    rows = cursor.fetchall()

    if (len(rows) == 0):
      return_value = False
    else:
      return_value = True

  cursor.close()
  return return_value

def insert_author_title(author_id, title_id, cnx):
  cursor = cnx.cursor()
  
  if not author_title_exists(author_id, title_id, cnx):
    insert_stmt = "INSERT INTO author_title (author_id, title_id) VALUES (%(author_id)s, %(title_id)s)"
    cursor.execute(insert_stmt, { 'author_id': author_id, 'title_id': title_id })
    cnx.commit()
    author_id = get_author_id(author, title_id, cnx)
    
  cursor.close()

def insert_book(title_id, price, cnx):
  cursor = cnx.cursor()
  
  insert_stmt = """ INSERT INTO book (listprice, ourprice, inventoried_when, 
                    location, status, distributor, title_id) VALUES 
                    (%(listprice)s, %(ourprice)s, %(inventoried_when)s,
                    %(location)s, %(status)s, %(distributor)s, %(title_id)s) """

  cursor.execute(insert_stmt, 
                 { 
                    'listprice': price, 
                    'ourprice': price,
                    'inventoried_when': datetime.now(),
                    'location': "Unknown",
                    'status': "STOCK",
                    'distributor': "?",
                    'title_id': title_id
                 })
  cnx.commit()
  cursor.close()

########################### BEGIN SCRIPT ########################### 

if (len(sys.argv) < 2):
  print("Usage: You must supply the csv file")
  sys.exit()

try: 
  #Set up db connection
  cnx = mysql.connector.connect(user=dbuser, password=dbpass, host=dbhost, database=dbname)
except Exception as e:
  print("Error connecting to database: " + str(e))
  sys.exit()

with open(sys.argv[1]) as f:
  for line in f:
    data = line.split("\t")
    isbn = data[0].strip() 
    title = data[1].strip()  
    author = re.sub("[']", "", data[2].strip() ) 
    try:
      price = float(data[3].strip())
    except ValueError:
      print("ValueError: " + str(data[3])) 
    binding = data[4].strip()  
    publisher = data[5].strip()  

    title_id = insert_title(isbn, title, price, binding, publisher, cnx)
    author_id = insert_author(author, title_id, cnx)
    insert_author_title(author_id, title_id, cnx)
    insert_book(title_id, price, cnx)

cnx.close()
