create database DVD_Rental_Company;

use DVD_Rental_Company;

create table BRANCH
(branch_number numeric(4,0), -- unique number assigned to each different branches
street varchar(20), -- address
city varchar(20),
state varchar(2) check (state in ('AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY')),
zip_code numeric(5,0),
telephone_number numeric(12,0) not null,
primary key (branch_number)
);

create table STAFF
(staff_number numeric(5,0), -- unique number assigned to each different staffs
branch_number numeric(4,0),
first_name varchar(20),
last_name varchar(20) not null,
position varchar(10),
salary numeric(10,2),
primary key (staff_number),
foreign key (branch_number) references BRANCH(branch_number)
);

create table MEMBER
(member_number numeric(9,0), -- unique number assigned to each different members
branch_number numeric(4,0),
first_name varchar(20),
last_name varchar(20) not null,
street varchar(20),
city varchar(20),
state varchar(2) check (state in ('AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY')),
zip_code numeric(5,0),
date_registered date,
primary key (member_number),
foreign key (branch_number) references BRANCH(branch_number)
);

create table CATEGORY
(category_id numeric(2,0), -- all unique categories
category_name varchar(35), -- the name of the category
primary key (category_id)
);

create table DIRECTOR
(director_id numeric(8,0), -- all unique directors
first_name varchar(20), -- their first name
last_name varchar(20) not null, -- their last name
primary key (director_id)
);

create table MAIN_ACTOR
(main_actor_id numeric(9,0), -- all unique main actors
first_name varchar(20), -- their first name
last_name varchar(20) not null, -- their last name
primary key (main_actor_id)
);

create table DVD
(catalog_number numeric(7,0), -- all unique DVDs
title varchar(100) not null, -- DVD title
category_id numeric(2,0), -- id of category
director_id numeric(8,0), -- id of directors
main_actor_id numeric(9,0), -- id of main actors
daily_rental numeric(4,2), -- rental cost of each DVD
cost numeric(5,2), -- cost of a particular DVD
primary key (catalog_number),
foreign key (category_id) references CATEGORY(category_id),
foreign key (director_id) references DIRECTOR(director_id),
foreign key (main_actor_id) references MAIN_ACTOR(main_actor_id)
);


create table DVD_DIRECTOR
(catalog_number numeric(7,0), -- all unique DVDs
director_id numeric(8,0), -- all unique directors
primary key (catalog_number, director_id),
foreign key (catalog_number) references DVD(catalog_number),
foreign key (director_id) references DIRECTOR(director_id)
);

create table DVD_MAIN_ACTOR
(catalog_number numeric(7,0), -- all unique DVDs
main_actor_id numeric(9,0), -- all unique main actors
primary key (catalog_number, main_actor_id),
foreign key (catalog_number) references DVD(catalog_number),
foreign key (main_actor_id) references MAIN_ACTOR(main_actor_id)
);

create table COPY
(DVD_number numeric(10,0), -- each unique DVD copies
catalog_number numeric(7,0) not null,
branch_number numeric(3,0) not null,
primary key (DVD_number),
foreign key (catalog_number) references DVD(catalog_number),
foreign key (branch_number) references BRANCH(branch_number)
);

create table RENT
(rental_number numeric(10,0), -- each unique rental number
member_number numeric(9,0),
DVD_number numeric(10,0),
date_rented datetime,
date_returned datetime,
status numeric(1,0) not null default 0 check (status = 0), --  any DVD copy shown in RENT table will not be available as 0 
primary key (rental_number, member_number, DVD_number),
foreign key (member_number) references MEMBER(member_number),
foreign key (DVD_number) references COPY(DVD_number)
);









