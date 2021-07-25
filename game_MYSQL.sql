CREATE DATABASE game_sql DEFAULT CHARACTER SET UTF8 COLLATE UTF8_GENERAL_CI;
CREATE USER 'pmauser'@'localhost' IDENTIFIED BY 'game0934';
GRANT ALL PRIVILEGES ON game_sql.* TO 'pmauser'@'localhost';

USE game_sql;

CREATE TABLE user_info(
    account VARCHAR(40) NOT NULL PRIMARY KEY, 
    password VARCHAR(40) NOT NULL, 
    name VARCHAR(40) NOT NULL, 
    play_status INT NOT NULL DEFAULT '0', 
    team_id INT NOT NULL DEFAULT '0'
);

CREATE TABLE user_item(
    account VARCHAR(40) NOT NULL PRIMARY KEY, 
    item_1 INT NOT NULL DEFAULT '0', 
    item_2 INT NOT NULL DEFAULT '0', 
    item_3 INT NOT NULL DEFAULT '0', 
    item_4 INT NOT NULL DEFAULT '0', 
    item_5 INT NOT NULL DEFAULT '0', 
    item_6 INT NOT NULL DEFAULT '0', 
    item_7 INT NOT NULL DEFAULT '0'
);

CREATE TABLE user_skill(
    account VARCHAR(40) NOT NULL PRIMARY KEY, 
    skill_1 INT NOT NULL DEFAULT '1', 
    skill_2 INT NOT NULL DEFAULT '1', 
    skill_3 INT NOT NULL DEFAULT '0', 
    skill_4 INT NOT NULL DEFAULT '0', 
    skill_u_1 INT NOT NULL DEFAULT '0', 
    skill_u_2 INT NOT NULL DEFAULT '0', 
    career varchar(40) NOT NULL DEFAULT 'x'
);

CREATE TABLE teams(
    leader varchar(40) NOT NULL DEFAULT '' PRIMARY KEY,
    member1 varchar(40) NOT NULL DEFAULT '', 
    member2 varchar(40) NOT NULL DEFAULT '', 
    member3 varchar(40) NOT NULL DEFAULT '', 
    id int
);


INSERT INTO `user_info` (account, password, name) VALUES ('test01', '0934', 'test01');
INSERT INTO `user_item` (account) VALUES ('test01');
INSERT INTO `user_skill` (account) VALUES ('test01');