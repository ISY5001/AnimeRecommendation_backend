CREATE DATABASE IF NOT EXISTS `user_data` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `user_data`;

CREATE TABLE IF NOT EXISTS `accounts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(40) NOT NULL,
  `email` varchar(100) NOT NULL,
  PRIMARY KEY(`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

//Ratings创表
CREATE TABLE IF NOT EXISTS `ratings` (
  `rate_id` int(11) NOT NULL AUTO_INCREMENT,
  `account_id` int(11) NOT NULL,
  `scores` int(2) NOT NULL, -- Adjust as per your needs. This allows scores like 4.5
  `anime_id` int(11) NOT NULL, -- or varchar, based on your ID system for animes
  PRIMARY KEY (`rate_id`),
  FOREIGN KEY (`account_id`) REFERENCES `accounts`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;