CREATE DATABASE IF NOT EXISTS `user_data` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `user_data`;

CREATE TABLE IF NOT EXISTS `accounts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(40) NOT NULL,
  `email` varchar(100) NOT NULL,
  PRIMARY KEY(`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- Ratings创表
CREATE TABLE IF NOT EXISTS `ratings` (
  `rate_id` int(11) NOT NULL AUTO_INCREMENT,
  `account_id` int(11) NOT NULL,
  `scores` int(2) NOT NULL, -- Adjust as per your needs. This allows scores like 4.5
  `anime_id` int(11) NOT NULL, -- or varchar, based on your ID system for animes
  PRIMARY KEY (`rate_id`),
  FOREIGN KEY (`account_id`) REFERENCES `accounts`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


SET GLOBAL local_infile=1;
-- create a temporary table to hold the data from the csv file
CREATE TEMPORARY TABLE temp_ratings (
  account_id INT,
  anime_id INT,
  scores INT
);

-- load the data from csv file into temp file
-- /Users/chenzhiwei/Desktop/AnimeRecommendation_backend/app/data/rating.csv
LOAD DATA LOCAL INFILE '/Users/chenzhiwei/Desktop/AnimeRecommendation_backend/app/data/rating.csv'
INTO TABLE temp_ratings
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- Select a limited number of rows from the temporary table:
INSERT INTO ratings (account_id, anime_id, scores)
SELECT account_id, anime_id, scores
FROM temp_ratings;
-- LIMIT 1000


-- Optionally, you can drop the temporary table:
DROP TEMPORARY TABLE temp_ratings;
