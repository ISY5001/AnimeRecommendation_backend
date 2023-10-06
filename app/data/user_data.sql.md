# Database : user_data 
```sql
CREATE DATABASE IF NOT EXISTS `user_data` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `user_data`;
```
## scripts for creating table `accounts`

```sql
CREATE TABLE IF NOT EXISTS `accounts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(40) NOT NULL,
  `email` varchar(100) NOT NULL,
  PRIMARY KEY(`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
```

## scripts for creating table `ratings`

```sql
-- run insert_random_id.py first if you haven't already
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
```

## scripts for creating `anime` table

```sql
CREATE TABLE IF NOT EXISTS anime (
  Anime_id INT NOT NULL,
  Title VARCHAR(255),
  Genre VARCHAR(255),
  Synopsis TEXT,
  Type VARCHAR(50),
  Producer VARCHAR(255),
  Studio VARCHAR(255),
  Rating FLOAT,
  ScoredBy INT,
  Popularity FLOAT,
  Members INT,
  Episodes INT,
  Source VARCHAR(255),
  Aired VARCHAR(255),
  Link VARCHAR(255),
  PRIMARY KEY (Anime_id)
);

-- /Users/chenzhiwei/Desktop/AnimeRecommendation_backend/app/data/Anime_data.csv
LOAD DATA LOCAL INFILE '/Users/chenzhiwei/Desktop/AnimeRecommendation_backend/app/data/Anime_data.csv'
INTO TABLE Anime
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
```

### add a new column in `anime`
```sql
ALTER TABLE anime ADD COLUMN poster VARCHAR(255);
```
