import MySQLdb

cursor=MySQLdb.connect('localhost', 'woodenshoe').cursor()
cursor.execute('SHOW DATABASES;')
databases=cursor.fetchall()
databases=[result[0] for result in databases if result[0] in ('infoshopkeeper', 'infoshopkeeper2')]
for dbase in databases:
    cursor.execute('USE %s;' % dbase)
    cursor.execute('SHOW TABLES FROM %s;' % dbase )
    tables=cursor.fetchall()
    
    for table in tables:
        cursor.execute("ALTER TABLE %s AUTO_INCREMENT=0;" %table[0])
        cursor.execute("DESCRIBE %s;" % table[0])
        table_descrip= cursor.fetchall()
        table_descrip= [ r[0] for r in table_descrip if r[3] == 'PRI']
        if table_descrip:
            cursor.execute("ALTER TABLE %s ORDER BY %s;" % (table[0], table_descrip[0]))
            cursor.execute("ALTER TABLE %s ENGINE = INNODB;" % table[0])

    cursor.execute('ALTER TABLE `author_title` ADD CONSTRAINT `author_pivot_FK` FOREIGN KEY (`author_id`) REFERENCES `author` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;')
    cursor.execute('DELETE  at1.* FROM `author_title` at1 LEFT JOIN `title` t1 ON t1.id=at1.title_id WHERE t1.id IS NULL;')
    cursor.execute('ALTER TABLE `author_title` ADD CONSTRAINT `author_pivot_FK` FOREIGN KEY (`author_id`) REFERENCES `author` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;')
    cursor.execute('ALTER TABLE `title` ADD CONSTRAINT `kind_fk` FOREIGN KEY (`kind_id`) REFERENCES `kind` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;')
    cursor.execute('DELETE b1.* FROM `book` b1 LEFT JOIN `title` t1 ON t1.id=b1.title_id WHERE t1.id IS NULL;')
    cursor.execute('ALTER TABLE `book` ADD CONSTRAINT `title_fk` FOREIGN KEY (`title_id`) REFERENCES `title` (`id`) ON UPDATE CASCADE ON DELETE RESTRICT;')
    cursor.execute('ALTER TABLE `book` ADD KEY `location_id` (`location_id`);')
    cursor.execute('ALTER TABLE `book` ALTER COLUMN `location_id` SET DEFAULT 1;')
    cursor.execute('ALTER TABLE `book` MODIFY `book`.`location_id` INT(11);')
    cursor.execute('ALTER TABLE `book` ADD CONSTRAINT `location_fk` FOREIGN KEY (`location_id`) REFERENCES `location` (`id`) ON UPDATE CASCADE ON DELETE SET NULL;')
