#!/usr/bin/python
import MySQLdb
import etc

new_db_conn=MySQLdb.connect (host = etc.dbhost,db=etc.dbname,user=etc.dbuser,passwd=etc.dbpass)
new=new_db_conn.cursor()

new.execute("""
ALTER TABLE transactionLog add paid_how varchar(20)
 
""")
