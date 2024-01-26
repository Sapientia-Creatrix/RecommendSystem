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

-- load data from csv file into table originData
LOAD DATA local INFILE 'E:\\progremmingFile\\Github\\Sapientia-Creatrix\\RecommendSystem\\Coursera_NewSkill.csv'
INTO TABLE originData
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- replace & with , in course_description column
UPDATE originData
SET course_description = REPLACE(course_description, '^', ',');


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
    popularity INT,
    deleted BOOLEAN
);

-- 將 originData 中的資料搬到 Course 中
INSERT INTO Course (name, university, url, difficulty, rate, description, skills, popularity, deleted)
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
    FLOOR(RAND() * 100001) AS popularity,
    CASE
        WHEN sepSkills = '' THEN 1
        ELSE 0
    END AS deleted
FROM originData;

describe Course;
SELECT COUNT(*) FROM Course;
select * from Course limit 1;


-- 創建存放 user 資料的 table
create table `user`(
	`id` int not null auto_increment,
    `name` varchar(128) not null,
    `gmail` varchar(128),
    `password_hash` varchar(1024) not null,
    `skills` varchar(2048),
    `learning_path` varchar(2048),
    `coin` int default 0,
    `skillPrefer` TEXT,
    `recommendHistory` TEXT,
	`deleted` boolean not null default false,
    primary key(`id`)
);
-- alter table `user` add column `password_hash` varchar(1024) not null after `name`;
-- alter table user add column `deleted` boolean not null default false;

INSERT INTO `user` (`name`, `password_hash`, `skills`, `learning_path`, `coin`, `skillPrefer`, `recommendHistory`) VALUES
('Jason', SHA2('password1', 512), 'Java,Python', '', 100, '{"Marketing": 0.25, "Data Science": 0.25, "Business": 0.2, "Computer Science": 0.15, "Data Analysis": 0.15, "Information Technology": 0.012, "Business Essentials": 0.012, "Business Strategy": 0.012, "Leadership and Management": 0.012, "Finance": 0.012, "Education": 0.002, "Personal Development": 0.002, "Software Development": 0.002, "Arts and Humanities": 0.002, "Machine Learning": 0.002, "Health": 0.002, "Physical Science and Engineering": 0.002, "Social Sciences": 0.002, "Data Management": 0.002, "Health Informatics": 0.002, "Probability and Statistics": 0.002, "Law": 0.002, "Psychology": 0.002, "Research": 0.002, "Economics": 0.002, "Chemistry": 0.002, "Other Languages": 0.002, "Support and Operations": 0.002, "Research Methods": 0.002, "Networking": 0.002, "Nutrition": 0.002, "Governance and Society": 0.002, "Basic Science": 0.002, "Cloud Computing": 0.002, "Entrepreneurship": 0.002, "History": 0.002, "Design and Product": 0.002, "Environmental Science and Sustainability": 0.002, "Computer Security and Networks": 0.002, "Patient Care": 0.002, "Algorithms": 0.002, "Math and Logic": 0.002, "Security": 0.002, "Philosophy": 0.002, "Physics and Astronomy": 0.002, "Learning English": 0.002}', '[{"course_id": 762, "RecommendOrder": 1, "RecommendFrequency": 1},{"course_id": 34, "RecommendOrder": 2, "RecommendFrequency": 3},{"course_id": 1192, "RecommendOrder": 3, "RecommendFrequency": 1}]');
INSERT INTO `user` (`name`, `password_hash`, `skills`, `learning_path`, `coin`, `skillPrefer`, `recommendHistory`) VALUES
('Dragon', SHA2('password2', 512), 'Java,Python', '', 100, '{"Marketing": 0.2, "Data Science": 0.3, "Business": 0.2, "Computer Science": 0.1, "Data Analysis": 0.2, "Information Technology": 0.012, "Business Essentials": 0.012, "Business Strategy": 0.012, "Leadership and Management": 0.012, "Finance": 0.012, "Education": 0.002, "Personal Development": 0.002, "Software Development": 0.002, "Arts and Humanities": 0.002, "Machine Learning": 0.002, "Health": 0.002, "Physical Science and Engineering": 0.002, "Social Sciences": 0.002, "Data Management": 0.002, "Health Informatics": 0.002, "Probability and Statistics": 0.002, "Law": 0.002, "Psychology": 0.002, "Research": 0.002, "Economics": 0.002, "Chemistry": 0.002, "Other Languages": 0.002, "Support and Operations": 0.002, "Research Methods": 0.002, "Networking": 0.002, "Nutrition": 0.002, "Governance and Society": 0.002, "Basic Science": 0.002, "Cloud Computing": 0.002, "Entrepreneurship": 0.002, "History": 0.002, "Design and Product": 0.002, "Environmental Science and Sustainability": 0.002, "Computer Security and Networks": 0.002, "Patient Care": 0.002, "Algorithms": 0.002, "Math and Logic": 0.002, "Security": 0.002, "Philosophy": 0.002, "Physics and Astronomy": 0.002, "Learning English": 0.002}', '[{"course_id": 11, "RecommendOrder": 1, "RecommendFrequency": 1},{"course_id": 22, "RecommendOrder": 2, "RecommendFrequency": 3},{"course_id": 33, "RecommendOrder": 3, "RecommendFrequency": 1}]');
INSERT INTO `user` (`name`, `password_hash`, `skills`, `learning_path`, `coin`, `skillPrefer`, `recommendHistory`) VALUES
('King', SHA2('password3', 512), 'social king', '', 100, '{"Marketing": 0, "Data Science": 0, "Business": 0, "Computer Science": 0, "Data Analysis": 0, "Information Technology": 0.012, "Business Essentials": 0.012, "Business Strategy": 0.012, "Leadership and Management": 0.012, "Finance": 0.012, "Education": 0.002, "Personal Development": 0.002, "Software Development": 0.002, "Arts and Humanities": 0.002, "Machine Learning": 0.002, "Health": 0.002, "Physical Science and Engineering": 0.002, "Social Sciences": 0.002, "Data Management": 0.002, "Health Informatics": 0.002, "Probability and Statistics": 0.9, "Law": 0.002, "Psychology": 0.002, "Research": 0.002, "Economics": 0.002, "Chemistry": 0.002, "Other Languages": 0.002, "Support and Operations": 0.002, "Research Methods": 0.002, "Networking": 0.002, "Nutrition": 0.002, "Governance and Society": 0.002, "Basic Science": 0.002, "Cloud Computing": 0.002, "Entrepreneurship": 0.002, "History": 0.002, "Design and Product": 0.002, "Environmental Science and Sustainability": 0.002, "Computer Security and Networks": 0.002, "Patient Care": 0.002, "Algorithms": 0.002, "Math and Logic": 0.002, "Security": 0.002, "Philosophy": 0.002, "Physics and Astronomy": 0.002, "Learning English": 0.002}', '[{"course_id": 111, "RecommendOrder": 1, "RecommendFrequency": 1},{"course_id": 222, "RecommendOrder": 2, "RecommendFrequency": 3},{"course_id": 333, "RecommendOrder": 3, "RecommendFrequency": 1}]');


create table `courseHistory`(
	`id` int not null auto_increment,
    `user_id` int not null,
    `course_id` int not null,
    `progress` float not null,
    foreign key(`user_id`) references `user`(`id`),
    foreign key(`course_id`) references `course`(`id`),
    primary key(`id`)
);


create table `badge`(
	`id` int not null auto_increment,
    `name` varchar(512) not null,
    `description` varchar(2048) not null,
    primary key(`id`)
);


create table `userBadge`(
	`id` int not null auto_increment,
    `user_id` int not null,
    `badge_id` int not null,
    `date` datetime default current_timestamp,
    `display` boolean default true,
    foreign key(`user_id`) references `user`(`id`),
    foreign key(`badge_id`) references `badge`(`id`),
    primary key(`id`, `user_id`, `badge_id`)
);


create table `courseComment`(
	`id` int not null auto_increment,
    `user_id` int not null,
    `course_id` int not null,
    `rate` float not null,
    `context` varchar(2048),
    foreign key(`user_id`) references `user`(`id`),
    foreign key(`course_id`) references `course`(`id`),
    primary key(`id`)
);


drop database main;



