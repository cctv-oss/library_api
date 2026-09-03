CREATE DATABASE library DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
use library;
create table books(
id INT PRIMARY KEY AUTO_INCREMENT,
title varchar(100) not null,
author varchar(50) not null,
price decimal(10,2) not null default 0.00,
stock int not null default 0,
publish date,
introduction text);