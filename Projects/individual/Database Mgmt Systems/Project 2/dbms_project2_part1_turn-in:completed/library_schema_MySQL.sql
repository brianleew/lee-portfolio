create database library;

use library;

show tables;

create table BOOK 
(title varchar(100),  
genre varchar(25),  
ISBN varchar(20), 
date_published date, 
publisher varchar(40), 
edition numeric(2,0), 
description varchar(300), 
primary key (ISBN) 
);

create table AUTHOR 
(author_id numeric(3,0), 
first_name varchar(20), 
midlde_name varchar(20), 
last_name varchar(20), 
primary key (author_id) 
);

create table BOOK_AUTHOR 
(ISBN varchar (20), 
author_id numeric(3,0), 
primary key (author_id, ISBN), 
foreign key (author_id) references AUTHOR(author_id), 
foreign key (ISBN) references BOOK(ISBN) 
);

create table COPY 
(barcode numeric(10,0), 
ISBN varchar(20), 
comment varchar(200), 
primary key (barcode), 
foreign key (ISBN) references BOOK(ISBN) 
);

create table MEMBER 
(card_no numeric(5,0), 
first_name varchar(20), 
middle_name varchar(20), 
last_name varchar(20), 
street varchar(20), 
city varchar(15), 
state varchar(2), 
apt_no numeric(5,0), 
zip_code numeric(5,0), 
phone_no numeric(12,0), 
email_address varchar(20), 
card_exp_date date, 
primary key (card_no) 
);

create table BORROW 
(card_no numeric(5,0), 
barcode numeric(10,0), 
date_borrowed datetime, 
date_returned datetime, 
renewals_no numeric(5,0), 
paid boolean, 
primary key (card_no, barcode, date_borrowed), 
foreign key (barcode) references COPY(barcode), 
foreign key (card_no) references MEMBER(card_no) 
);