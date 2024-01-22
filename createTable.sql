-- 這支程式是用來在本地建立資料庫及專案所需 table 的

create database if not exists main;
use main;


-- create table originData
CREATE TABLE if not exists originData (
    course_name VARCHAR(255),
    university VARCHAR(255),
    difficulty_level VARCHAR(50),
    course_rating FLOAT,
    course_url VARCHAR(255),
    course_description TEXT,
    skills TEXT,
    sepSkills TEXT
);

--load data from csv file into table originData
LOAD DATA local INFILE 'E:\\progremmingFile\\Github\\Sapientia-Creatrix\\Coursera_NewSkill.csv'
INTO TABLE originData
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- replace & with , in course_description column
UPDATE originData
SET course_description = REPLACE(course_description, '&', ',');


describe originData;
SELECT COUNT(*) FROM originData;


CREATE TABLE if not exists Course (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    university VARCHAR(255),
    url VARCHAR(255),
    difficulty ENUM('Conversant', 'Advanced', 'Beginner', 'Intermediate', 'Not Calibrated'),
    rate FLOAT,
    description TEXT,
    skills TEXT,
    deleted BOOLEAN
);

-- 將 originData 中的資料搬到 Course 中
INSERT INTO Course (name, university, url, difficulty, rate, description, skills, deleted)
SELECT
    course_name,
    university,
    course_url,
    CASE
        WHEN difficulty_level = 'Conversant' THEN 'Conversant'
        WHEN difficulty_level = 'Advanced' THEN 'Advanced'
        WHEN difficulty_level = 'Beginner' THEN 'Beginner'
        WHEN difficulty_level = 'Intermediate' THEN 'Intermediate'
        WHEN difficulty_level = 'Not Calibrated' THEN 'Not Calibrated'
        ELSE NULL
    END,
    course_rating,
    course_description,
    sepSkills,
    CASE
        WHEN sepSkills = '' THEN 1
        ELSE 0
    END AS deleted
FROM originData;

describe Course;
SELECT COUNT(*) FROM Course;
select * from Course limit 1;


drop database main;



