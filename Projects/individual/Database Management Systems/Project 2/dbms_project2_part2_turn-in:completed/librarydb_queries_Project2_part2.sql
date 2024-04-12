
-- 1. For each library member his card number, first, middle and last name along with the number of book copies he ever borrowed. There may be members who didn't ever borrow any book copy.
-- ------------------------------
select card_no, first_name, middle_name, last_name, count(distinct barcode)
from MEMBER natural join BORROW
group by card_no;
-- ________________________________
-- 2. Members (their card numbers, first, middle and last names) who held a book copy the longest. 
-- There can be one such member or more than one. 
-- Don't take into accout a case that someone borrowed the same book copy again.
-- Don't take into account members who borrowed a book copy and didn't return it yet.
-- --------------------------------
select card_no, first_name, middle_name, last_name
from MEMBER natural join BORROW
where datediff(date_returned,date_borrowed) = (select max(datediff(date_returned,date_borrowed)) from BORROW);
-- ________________________________
-- 3. For each book (ISBN and title) the number of copies the library owns.
-- --------------------------------
select ISBN, title, count(ISBN)
from BOOK natural join COPY
group by ISBN, title;
-- ________________________________
-- 4. Books (ISBNs and titles), if any, having exactly 3 authors.
-- --------------------------------
select ISBN, title
from BOOK_AUTHOR natural join BOOK
group by ISBN, title
having count(ISBN) = 3;
-- ________________________________
-- 5. For each author (ID, first, middle and last name) the number of books he wrote.
-- --------------------------------
select author_id, first_name, middle_name, last_name, count(author_id)
from BOOK_AUTHOR natural join AUTHOR
group by author_id;
-- ________________________________
-- 6. Card number, first, middle and last name of members, if any, who borrowed some book by Chartrand(s). 
-- Remove duplicates from the result.
-- --------------------------------
select card_no, first_name, middle_name, last_name
from MEMBER natural join BORROW
where card_no in (select card_no
from AUTHOR natural join BOOK_AUTHOR natural join COPY natural join BORROW
where AUTHOR.last_name = 'Chartrand')
group by card_no;
-- ________________________________
-- 7. Most popular author(s) (their IDs and first, middle and last names) in the library.
-- --------------------------------
select author_id, first_name, middle_name, last_name
from BORROW natural join COPY natural join BOOK_AUTHOR natural join AUTHOR
group by barcode, author_id
having count(barcode) = (select MAX(bt.bc)
from (select count(barcode) as bc
from BORROW 
group by barcode) as bt);
-- ________________________________
-- 8. Card numbers, first, middle, last names and addresses of members whose libray card will expire within the next month.
-- --------------------------------
select card_no, first_name, middle_name, last_name, street, city, state, apt_no, zip_code
from MEMBER
where card_exp_date >= now() and card_exp_date <= DATE_ADD(now(),INTERVAL 30 DAY);
-- ________________________________
-- 9. Card numbers, first, middle and last names of members along with the amount of money they owe to the library. 
-- Assume that if a book copy is returned one day after the due date, a member owes 0.25 cents to the library.
-- --------------------------------
select card_no, first_name, middle_name, last_name, sum(datediff(now(), date_add(date_borrowed, interval renewals_no * 14 DAY)) * .25)
from BORROW natural join MEMBER
where date_returned is NULL and renewals_no <= 2 and datediff(now(), date_add(date_borrowed, interval renewals_no * 14 DAY)) > 14 
group by card_no;
-- ________________________________
-- 10. The amount of money the library earned (received money for) from late returns.
-- --------------------------------
select sum(datediff(now(), date_add(date_borrowed, interval renewals_no * 14 DAY)) * .25)
from BORROW
where paid = 1 and date_returned is NULL and renewals_no <= 2 and datediff(now(), date_add(date_borrowed, interval renewals_no * 14 DAY)) > 14;
-- ________________________________
-- 11. Members (their card numbers, first, middle and last names) who borrowed more non-fiction books than fiction books.
-- --------------------------------
select card_no, first_name, middle_name, last_name
from BOOK natural join GENRE natural join MEMBER natural join BORROW natural join COPY
group by card_no, type
having count(type) in (select count(type)
from BOOK natural join GENRE natural join MEMBER natural join BORROW natural join COPY
group by card_no, type
having type = 1) > count(type) in (select count(type)
from BOOK natural join GENRE natural join MEMBER natural join BORROW natural join COPY
group by card_no, type
having type = 0);
-- ________________________________
-- 12. Name of the most popular publisher(s).
select publisher
from (select publisher
from BORROW natural join COPY natural join BOOK
group by publisher, card_no) as temp
group by publisher
having count(publisher) = (select max(pt.pc) 
from (select count(publisher) as pc 
from (select publisher
from BORROW natural join COPY natural join BOOK
group by publisher, card_no) as temp
group by publisher) as pt);
-- WRITE_YOUR_QUERY_HERE for 12.
-- ________________________________
-- 13. Members (card numbers, first, middle and last names) who never borrowed any book copy and whose card expired.
-- --------------------------------
select card_no, first_name, middle_name, last_name
from MEMBER
where card_no not in (select card_no from BORROW) and card_exp_date < now();
-- ________________________________
-- 14. The most popular genre(s).
-- --------------------------------
select name
from (select name 
from BORROW natural join COPY natural join BOOK natural join GENRE 
group by name, card_no) as temp
group by name
having count(name) = (select max(nt.nc) 
from (select count(name) as nc
from (select name
from BORROW natural join COPY natural join BOOK natural join GENRE
group by name, card_no) as temp
group by name) as nt);
-- ________________________________
-- 15. For each state, in which some member lives, the most popular last name(s). 
-- --------------------------------
select state, last_name
from MEMBER
group by state, last_name
having count(last_name) = (select MAX(lnt.lnc) from (select last_name, count(last_name) as lnc from MEMBER group by state, last_name) as lnt);
-- ________________________________
-- 16. Books (ISBNs and titles) that don't have any authors. 
-- --------------------------------
select ISBN, title
from BOOK
where BOOK.ISBN not in (select ISBN from BOOK_AUTHOR);
-- ________________________________
-- 17. Members (card numbers) who borrowed the same book more than once (not necessarily the same copy of a book).
-- --------------------------------
select distinct card_no
from MEMBER natural join BORROW natural join COPY
group by card_no, ISBN
having count(ISBN) > 1;
-- ________________________________
-- 18. Number of members from Cookeville, TN and from Algood, TN.
-- --------------------------------
select count(card_no)
from MEMBER
where city = 'Cookeville' or 'Algood' and state = 'TN';
-- ________________________________
-- 19. Card numbers and emails of members who should return a book copy tomorrow. If these members didn't renew their loan twice, then they still have a chance to renew their loan. If they won't renew or return a book tomorrow, then they will be charged for the following day(s).
-- --------------------------------
select card_no, email_address
from MEMBER natural join BORROW
where date_returned is null and 
(renewals_no = 0 and date_add(date_borrowed, interval 13 DAY) = now()) 
or 
(renewals_no = 1 and date_add(date_borrowed, interval 27 DAY) = now())
or
(renewals_no = 2 and date_add(date_borrowed, interval 41 DAY) = now());
-- ________________________________
-- 20. Condition of a book copy that was borrowed the most often, not necessarily held the longest.
-- --------------------------------
select barcode, comment
from BORROW natural join COPY
group by barcode
having count(barcode) = (select MAX(bt.bc)
from (select count(barcode) as bc
from BORROW 
group by barcode) as bt);
-- ________________________________