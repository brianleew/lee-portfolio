-- 1. For each member (card number, first, middle and last name) and for each genre type, how many book copies of the type the member borrowed.
-- If a member borrowed a given book more then once, it should be counted once.
-- If the member Jen, Karen Green with card number 1 borrowed 5 non-fiction books and 0 fiction books, then the following tuples should be in the result of the query.
-- 1 | Jen | Karen | Green | 1 | 5
-- 1 | Jen | Karen | Green | 0 | 0
-- ------------------------------
select card_no, first_name, middle_name, last_name, type, ifnull(k, 0) as count_bookCopyType
from
(select card_no, type
from BORROW natural join COPY natural join BOOK natural left outer join ((select 1) union (select 0)) as t (type)
group by card_no, type) as main
natural left outer join 
(select card_no, type, count(type) as k
from (
select card_no, barcode, type
from BORROW natural join COPY natural join BOOK natural left outer join GENRE
group by card_no, barcode
) as p
group by card_no, type) as part 
natural join MEMBER;
-- ________________________________
-- 2. For every author (ID, first, middle and last name), how many books he is an author of.
-- There can be authors not associated with any book.
-- --------------------------------
select author_id, first_name, middle_name, last_name, count(distinct ISBN) as count_books
from author natural left outer join book_author
group by author_id;
-- ________________________________
-- 3. For every book copy (barcode, ISBN and title), how many times it was borrowed.
-- There can be book copies that were never borrowed.
-- --------------------------------
select barcode, ISBN, title, ifnull(k, 0) as count_wasBorrowed
from COPY natural join BOOK natural left outer join (select barcode, count(barcode) as k from BORROW group by barcode) as temp;
-- ________________________________
-- 4. For every member (card number, first, middle and last name), how many loans he paid a late fee for.
-- --------------------------------
select card_no, first_name, middle_name, last_name, ifnull(k, 0) as paid_loan
from MEMBER 
natural left outer join 
(select sum(datediff(now(), date_add(date_borrowed, interval renewals_no * 14 DAY)) * .25) as k
from BORROW
where paid = 1 and date_returned is NULL and renewals_no <= 2 and datediff(now(), date_add(date_borrowed, interval renewals_no * 14 DAY)) > 14) as temp;
-- ________________________________
-- 5. For every first, middle and last name in the database, the number of authors who have it and the number of members who have it.
-- If there is 1 author named Jen, Karen Green and two members named Jen, Karen Green, then the following tuple should be in the result of the query.
-- Jen | Karen | Green | 1 | 2
-- --------------------------------
with temp1(first_name,middle_name,last_name, ca, cm) as
(select first_name,middle_name,last_name, ca, cm from
(select first_name, middle_name, last_name, count(card_no) as cm
from MEMBER
group by first_name,middle_name,last_name) as m
natural left outer join
(select first_name, middle_name, last_name, count(author_id) as ca
from AUTHOR
group by first_name, middle_name, last_name) as a
group by first_name, middle_name, last_name),
temp2(first_name,middle_name,last_name, ca, cm) as
(select first_name,middle_name,last_name, ca, cm from
(select first_name, middle_name, last_name, count(card_no) as cm
from MEMBER
group by first_name,middle_name,last_name) as m
natural right outer join
(select first_name, middle_name, last_name, count(author_id) as ca
from AUTHOR
group by first_name,middle_name,last_name) as a
group by first_name,middle_name,last_name)
select first_name,middle_name,last_name, sum(ifnull(ca, 0)) as numOfAuthor, sum(ifnull(cm, 0)) as numOfMember
from
(select * from temp1 natural left outer join temp2
union
select * from temp1 natural right outer join temp2) as temp
group by first_name,middle_name,last_name;
-- ________________________________
-- 6. For every member (card number, first, middle and last name), how many book copies they borrowed in 2020, 2021 and 2022.
-- If there is a member named Jen, Karen Green with card number 1, and she borrowed 10 book copies in 2021, 5 in 2022 and none in 2020, then the following tuple should be in the result of the query.analyze
-- 1 | Jen | Karen | Green | 0 | 10 | 5
-- --------------------------------
select card_no, first_name, middle_name, last_name, ifnull(p,0) as '2020', ifnull(b,0) as '2021', ifnull(n,0) as '2022'
from MEMBER 
natural left outer join
(select card_no, count(distinct barcode) as p
from BORROW
where year(date_borrowed) = 2020
group by card_no) as pp
natural left outer join
(select card_no, count(distinct barcode) as b
from BORROW
where year(date_borrowed) = 2021
group by card_no) as bb
natural left outer join
(select card_no, count(distinct barcode) as n
from BORROW
where year(date_borrowed) = 2022
group by card_no) as nn;
-- ________________________________
-- 7. Starting from the first year in which some book copy was borrowed (do not assume any specific value), for each year, for each month of the year, how many book copies were borrowed that month.
-- 2021 | 0 | 1 | 10 | 11 | 1 | 2 | 3 | 2 | 10 | 11 | 12 | 3 <--- 0 book copies were borrowed in January, 1 in Feb, 10 in March etc.
-- 2022 | 1 | 2 | 5 | 21 | 23 | 12 | 6 | 2 | 7 | 1 | 0 | 0
-- You may find this helpful ---> https://stackoverflow.com/questions/626797/sql-to-return-list-of-years-since-a-specific-year .
-- --------------------------------
select year, ifnull(January,0) as January, ifnull(February,0) as February,ifnull(March,0) as March, ifnull(April,0) as April, ifnull(May,0) as May, ifnull(June,0) as June, ifnull(July,0) as July, ifnull(August,0) as August, ifnull(September,0) as September, ifnull(October,0) as October, ifnull(November,0) as November, ifnull(December,0) as December from
(with recursive yearlist (year) as
(   select min(year(date_borrowed)) as year from BORROW
    union all
    select yl.year + 1 as year
    from yearlist yl
    where yl.year + 1 <= YEAR(now())
)
select year from yearlist order by year asc) as years
natural left outer join
(select count(distinct barcode) as January, year(date_borrowed) as year
from BORROW 
where month(date_borrowed) = 1
group by year(date_borrowed)) as jan_t
natural left outer join
(select count(distinct barcode) as February, year(date_borrowed) as year
from BORROW 
where month(date_borrowed) = 2
group by year(date_borrowed)) as feb_t
natural left outer join
(select count(distinct barcode) as March, year(date_borrowed) as year
from BORROW 
where month(date_borrowed) = 3
group by year(date_borrowed)) as mar_t
natural left outer join
(select count(distinct barcode) as April, year(date_borrowed) as year
from BORROW 
where month(date_borrowed) = 4
group by year(date_borrowed)) as apr_t
natural left outer join
(select count(distinct barcode) as May, year(date_borrowed) as year
from BORROW 
where month(date_borrowed) = 5
group by year(date_borrowed)) as may_t
natural left outer join
(select count(distinct barcode) as June, year(date_borrowed) as year
from BORROW 
where month(date_borrowed) = 6
group by year(date_borrowed)) as jun_t
natural left outer join
(select count(distinct barcode) as July, year(date_borrowed) as year
from BORROW 
where month(date_borrowed) = 7
group by year(date_borrowed)) as jul_t
natural left outer join
(select count(distinct barcode) as August, year(date_borrowed) as year
from BORROW 
where month(date_borrowed) = 8
group by year(date_borrowed)) as aug_t
natural left outer join
(select count(distinct barcode) as September, year(date_borrowed) as year
from BORROW 
where month(date_borrowed) = 9
group by year(date_borrowed)) as sep_t
natural left outer join
(select count(distinct barcode) as October, year(date_borrowed) as year
from BORROW 
where month(date_borrowed) = 10
group by year(date_borrowed)) as oct_t
natural left outer join
(select count(distinct barcode) as November, year(date_borrowed) as year
from BORROW 
where month(date_borrowed) = 11
group by year(date_borrowed)) as nov_t
natural left outer join
(select count(distinct barcode) as December, year(date_borrowed) as year
from BORROW 
where month(date_borrowed) = 12
group by year(date_borrowed)) as dec_t;
-- ________________________________
-- 8. For each member (card number, first, middle and last name) the last day he borrowed anything and how many book copies he borrowed that day.
-- --------------------------------
select card_no, first_name, last_name, middle_name, last_day_borrowed, ifnull(many,0) as num_book_copies from 
MEMBER
natural left outer join
(select card_no, date_borrowed as last_day_borrowed, count(distinct barcode) as many from
(select card_no, max(date_borrowed) as date_borrowed
from BORROW
group by card_no) as high
natural join
(select * from BORROW) as e
group by card_no) as p;
-- ________________________________
-- 9. For each book (ISBN and title), the number of authors and the number of copies the library owns.
-- --------------------------------
select ISBN, title, ifnull(num_author,0) as number_of_authors, ifnull(num_copy,0) as number_of_copies from
(select ISBN,title
from BOOK group by ISBN) as main
natural left outer join
(select ISBN, count(distinct barcode) as num_copy
from COPY
group by ISBN) as num_copy_table
natural left outer join
(select ISBN, count(distinct author_id) as num_author
from BOOK_AUTHOR
group by ISBN) as num_author_table;
-- ________________________________
-- 10. For each book (ISBN and title) the number of members who borrowed some of its copies and returned it on the same day.
-- --------------------------------
select ISBN, title, ifnull(num_member,0) as number_of_members
from BOOK
natural left outer join 
(select ISBN, count(distinct card_no) as num_member from
(select card_no, cast(date_borrowed AS date) as same, ISBN
from BORROW natural join COPY
where date_borrowed is not null) as borrow_table
natural join
(select card_no, cast(date_returned AS date) as same, ISBN
from BORROW natural join COPY
where date_returned is not null) as return_table
group by ISBN) as t3;