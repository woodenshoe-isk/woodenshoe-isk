-- MySQL dump 10.13  Distrib 5.5.50, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: infoshopkeeper
-- ------------------------------------------------------
-- Server version	5.5.50-0ubuntu0.14.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `ISBN_to_be_entered`
--

DROP TABLE IF EXISTS `ISBN_to_be_entered`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ISBN_to_be_entered` (
  `isbn` char(15) NOT NULL,
  `location` char(50) NOT NULL,
  `count` bigint(20) NOT NULL DEFAULT '0',
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `location_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=163 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `author`
--

DROP TABLE IF EXISTS `author`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `author` (
  `title_id` int(11) DEFAULT NULL,
  `author_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `author_name_2` (`author_name`),
  KEY `author_name` (`author_name`),
  KEY `title_id` (`title_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17888 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `author_title`
--

DROP TABLE IF EXISTS `author_title`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `author_title` (
  `author_id` int(11) DEFAULT NULL,
  `title_id` int(11) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_author_title` (`author_id`,`title_id`),
  KEY `author_id` (`author_id`),
  KEY `title_id` (`title_id`),
  CONSTRAINT `author_pivot_FK` FOREIGN KEY (`author_id`) REFERENCES `author` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `title_pivot_FK` FOREIGN KEY (`title_id`) REFERENCES `title` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=26283 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `book`
--

DROP TABLE IF EXISTS `book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `book` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `listprice` decimal(10,2) DEFAULT '0.00',
  `ourprice` float(10,2) DEFAULT '0.00',
  `consignment_status` varchar(255) CHARACTER SET utf8 COLLATE utf8_icelandic_ci DEFAULT NULL,
  `inventoried_when` date DEFAULT NULL,
  `type` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `location` varchar(50) COLLATE utf8_unicode_ci NOT NULL DEFAULT ' ',
  `location_id` int(11) DEFAULT NULL,
  `status` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `distributor` varchar(127) COLLATE utf8_unicode_ci NOT NULL DEFAULT ' ',
  `title_id` int(11) DEFAULT NULL,
  `sold_when` date DEFAULT NULL,
  `owner` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `notes` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `wholesale` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `title_id` (`title_id`),
  KEY `status` (`status`),
  KEY `location_id` (`location_id`),
  CONSTRAINT `location_fk` FOREIGN KEY (`location_id`) REFERENCES `location` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `title_fk` FOREIGN KEY (`title_id`) REFERENCES `title` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=59480 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `book_inventory`
--

DROP TABLE IF EXISTS `book_inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `book_inventory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `isbn` char(15) CHARACTER SET latin1 NOT NULL,
  `ourprice` float DEFAULT NULL,
  `location` char(50) CHARACTER SET latin1 NOT NULL,
  PRIMARY KEY (`id`),
  KEY `isbn` (`isbn`) USING BTREE,
  KEY `ourprice` (`ourprice`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=3558 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cashbox`
--

DROP TABLE IF EXISTS `cashbox`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cashbox` (
  `amount` float DEFAULT NULL,
  `date` datetime DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `category` (
  `title_id` int(11) DEFAULT NULL,
  `category_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT ' ',
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=147135 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cd`
--

DROP TABLE IF EXISTS `cd`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cd` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `isbn` char(15) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `isbn` (`isbn`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=557 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cover`
--

DROP TABLE IF EXISTS `cover`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cover` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `isbn` char(15) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `location` char(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `isbn` (`isbn`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=373 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `images`
--

DROP TABLE IF EXISTS `images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `images` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title_id` int(11) DEFAULT NULL,
  `small_url` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `med_url` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `large_url` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `created_at` date DEFAULT NULL,
  `updated_at` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11141 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kind`
--

DROP TABLE IF EXISTS `kind`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kind` (
  `kind_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `location`
--

DROP TABLE IF EXISTS `location`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `location` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `location_name` varchar(128) COLLATE utf8_unicode_ci NOT NULL DEFAULT ' ',
  PRIMARY KEY (`id`),
  KEY `location_name` (`location_name`),
  KEY `location` (`location_name`)
) ENGINE=InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `music`
--

DROP TABLE IF EXISTS `music`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `music` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `isbn` char(15) COLLATE utf8_unicode_ci NOT NULL,
  `location` char(50) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `isbn` (`isbn`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=352 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `notes`
--

DROP TABLE IF EXISTS `notes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `notes` (
  `message` text COLLATE utf8_unicode_ci,
  `author` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `whenEntered` datetime DEFAULT NULL,
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=461 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ranked_database`
--

DROP TABLE IF EXISTS `ranked_database`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ranked_database` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title_id` int(11) DEFAULT NULL,
  `isbn` char(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `kind_id` int(11) DEFAULT NULL,
  `ourprice` float DEFAULT NULL,
  `book_id` int(11) DEFAULT NULL,
  `RANK` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `title_id` (`title_id`) USING BTREE,
  KEY `isbn` (`isbn`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=6162 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ranked_inventory`
--

DROP TABLE IF EXISTS `ranked_inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ranked_inventory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `isbn` char(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ourprice` float DEFAULT NULL,
  `location` char(50) CHARACTER SET latin1 NOT NULL,
  `RANK` bigint(22) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `isbn` (`isbn`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=3372 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `schema_migrations`
--

DROP TABLE IF EXISTS `schema_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `schema_migrations` (
  `version` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  UNIQUE KEY `unique_schema_migrations` (`version`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `special_order`
--

DROP TABLE IF EXISTS `special_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `special_order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_ordered` date NOT NULL,
  `customer_name` varchar(64) DEFAULT '',
  `customer_phone_number` varchar(32) DEFAULT NULL,
  `customer_email` varchar(254) DEFAULT '',
  `customer_order` text,
  `other_notes` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `status`
--

DROP TABLE IF EXISTS `status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `status` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` char(8) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci PACK_KEYS=1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `title`
--

DROP TABLE IF EXISTS `title`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `title` (
  `id` int(16) NOT NULL AUTO_INCREMENT,
  `isbn` varchar(13) COLLATE utf8_unicode_ci NOT NULL DEFAULT ' ',
  `booktitle` text COLLATE utf8_unicode_ci,
  `publisher` varchar(50) COLLATE utf8_unicode_ci NOT NULL DEFAULT ' ',
  `release_date` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `tag` text COLLATE utf8_unicode_ci,
  `kind_id` int(11) DEFAULT NULL,
  `edition` int(11) DEFAULT NULL,
  `type` varchar(25) COLLATE utf8_unicode_ci DEFAULT NULL,
  `orig_isbn` varchar(13) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `isbn` (`isbn`),
  KEY `booktitle` (`booktitle`(25)),
  KEY `kind_id` (`kind_id`),
  CONSTRAINT `kind_fk` FOREIGN KEY (`kind_id`) REFERENCES `kind` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=16186 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `title_special_order`
--

DROP TABLE IF EXISTS `title_special_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `title_special_order` (
  `id` int(16) unsigned NOT NULL AUTO_INCREMENT,
  `title_id` int(16) NOT NULL,
  `special_order_id` int(11) NOT NULL,
  `order_status` varchar(16) NOT NULL DEFAULT '',
  `placed_when` date DEFAULT NULL,
  `ordered_when` date DEFAULT NULL,
  `arrived_when` date DEFAULT NULL,
  `finished_when` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `title_id` (`title_id`),
  KEY `special_order_id` (`special_order_id`),
  KEY `order_status` (`order_status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `transactionLog`
--

DROP TABLE IF EXISTS `transactionLog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `transactionLog` (
  `action` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `amount` float DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  `cashier` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `info` blob,
  `schedule` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `owner` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `paid_how` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cart_id` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=56286 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `type`
--

DROP TABLE IF EXISTS `type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `type` (
  `type_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-09-04 22:36:54
