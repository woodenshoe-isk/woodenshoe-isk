#!/usr/bin/env python3

# This script is used to inventory the isbns that are 
# into the database. 

from config.etc import *
from datetime import datetime

import mysql.connector
import sys

########################### FUNCTIONS ########################### 

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

  return return_value

def insert_book(title_id, price, cnx):
  cursor = cnx.cursor()
  
  insert_stmt = """ INSERT INTO book (listprice, ourprice, inventoried_when, 
                    location, location_id, status, distributor, title_id) VALUES 
                    (%(listprice)s, %(ourprice)s, %(inventoried_when)s,
                    %(location)s, %(location_id)s, %(status)s, %(distributor)s, %(title_id)s) """

  cursor.execute(insert_stmt, 
                 { 
                    'listprice': price, 
                    'ourprice': price,
                    'inventoried_when': datetime.now(),
                    'location': "Unknown",
                    'location_id': 136,
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
    try:
      price = float(data[1].strip())
    except ValueError:
      print("ValueError: " + str(isbn) + "\n")

    title_id = get_title_id(isbn, cnx)
    insert_book(title_id, price, cnx)

cnx.close()
