DROP DATABASE IF EXISTS testbook;
CREATE DATABASE testbook DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE testbook;
CREATE TABLE book(
    id int PRIMARY KEY auto_increment,
    bookname VARCHAR(64) not null,
    link varchar(128),
    come_from varchar(128),
    pic varchar(128),
    author varchar(64),
    publish varchar(32),
    depict varchar(256),
    price decimal(6,2),
    price_r decimal(6,2),
    grade int,
    valid boolean default 1
);


CREATE TABLE user
(
    id int PRIMARY KEY auto_increment,
    username varchar(32) not null,
    nickname varchar(32),
    email varchar(32),
    phone varchar(32),
    gender int,
    age int,  
    passwd varchar(64) not null,
    valid boolean default 1
);

CREATE TABLE manager
(
    id int PRIMARY KEY auto_increment,
    username varchar(32) not null,
    passwd varchar(64) not null,
    valid bool default 1
);
