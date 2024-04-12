use library;

SET SQL_SAFE_UPDATES = 0;

delete from book_author;
delete from borrow;
delete from copy;
delete from author;
delete from book;
delete from member;

insert into BOOK values ('Discrete Mathematics', 'Textbook', '978-1-57766-730-8', '2011-01-01', 'Waveland Press, Inc.', 1, 'Textbook for the "Discrete Structures of the CS" college level course.'); 
insert into BOOK values ('Alice in Wonderland', 'fiction', '979-8749522310', '2021-05-06', 'Independently published', 1, 'This edition of the book includes original illustrations.'); 
insert into BOOK values ('Green Eggs and Ham', 'Childrens literature', '978-0375810886', '2001-01-01', 'Random House Books for Young Readers', 1, 'One of the most famous books by Dr. Seuss.'); 
insert into BOOK values ('The Body Keeps the Score', 'non-fiction', '978-0143127741', '2015-09-08', 'Penguin Publishing Group', 1, 'A book on trauma.'); 
insert into BOOK values ('Little Women', 'Coming of age', '978-1950435098', '2019-03-02', 'SeaWolf Press', 1, 'A coming-of-age novel written in 1868.'); 
insert into BOOK values ('Introduction to Automata Theory, Languages, and Computation', 'Textbook', '978-0321455369', '2006-06-29', 'Pearson', 3, 'Book on formal languages, automata theory, and computational complexity.'); 
insert into BOOK values ('Database Systems: A Practical Approach to Design, Implementation, and Management', 'Textbook', '978-0132943260', '2014-01-08',  'Pearson', 6, 'Ideal for a one or two term course in database management or database design in an undergraduate or graduate level.'); 
insert into BOOK values ('Oregon Archaeology', 'History', '978-0870716065', '2011-10-01', 'Oregon State University Press', 1, 'Recent archeological findings on the history of Oregon.'); 
insert into BOOK values ('Compilers: Principles, Techniques, and Tools', 'textbook', '978-0321486813', '2006-08-31', 'Addison Wesley', 2, 'On software engineering, programming languages, and computer architecture.'); 

insert into AUTHOR values (0, 'Gary', null, 'Chartrand'); 
insert into AUTHOR values (1, 'Ping', null, 'Zhang'); 
insert into AUTHOR values (2, 'Levis', null, 'Carroll'); 
insert into AUTHOR values (3, 'Theodor', null, 'Seuss'); 
insert into AUTHOR values (4, 'Bessel', null, 'van der Kolk'); 
insert into AUTHOR values (5, 'Louisa', 'May', 'Alcott'); 
insert into AUTHOR values (6, 'John', 'E.', 'Hopcroft'); 
insert into AUTHOR values (7, 'Rajeev', null, 'Motwani'); 
insert into AUTHOR values (8, 'Jeffrey', 'D.', 'Ullman'); 
insert into AUTHOR values (9, 'Thomas', 'M.', 'Connolly'); 
insert into AUTHOR values (10, 'Carolyn', 'E.', 'Begg'); 
insert into AUTHOR values (11, 'Melvin', 'C.', 'Aikens'); 
insert into AUTHOR values (12, 'Thomas', 'J.', 'Connolly'); 
insert into AUTHOR values (13, 'Dennis', 'L.', 'Jenkins'); 
insert into AUTHOR values (14, 'Alfred', 'V.', 'Aho'); 
insert into AUTHOR values (15, 'Monica', 'S.', 'Lam'); 
insert into AUTHOR values (16, 'Ravi', null, 'Sethi');

insert into BOOK_AUTHOR values ('978-1-57766-730-8', 0); 
insert into BOOK_AUTHOR values ('978-1-57766-730-8', 1); 
insert into BOOK_AUTHOR values ('979-8749522310', 2); 
insert into BOOK_AUTHOR values ('978-0375810886', 3); 
insert into BOOK_AUTHOR values ('978-0143127741', 4); 
insert into BOOK_AUTHOR values ('978-1950435098', 5); 
insert into BOOK_AUTHOR values ('978-0321455369', 6); 
insert into BOOK_AUTHOR values ('978-0321455369', 7); 
insert into BOOK_AUTHOR values ('978-0321455369', 8); 
insert into BOOK_AUTHOR values ('978-0132943260', 9); 
insert into BOOK_AUTHOR values ('978-0132943260', 10); 
insert into BOOK_AUTHOR values ('978-0870716065', 11); 
insert into BOOK_AUTHOR values ('978-0870716065', 12); 
insert into BOOK_AUTHOR values ('978-0870716065', 13); 
insert into BOOK_AUTHOR values ('978-0321486813', 8); 
insert into BOOK_AUTHOR values ('978-0321486813', 14); 
insert into BOOK_AUTHOR values ('978-0321486813', 15); 
insert into BOOK_AUTHOR values ('978-0321486813', 16); 

insert into copy values (1100, '978-1-57766-730-8', null); 
insert into copy values (1101, '978-0132943260', null); 
insert into copy values (1102, '978-0132943260', null); 
insert into copy values (1103, '978-0132943260', 'Pencil on about 10 pages.'); 
insert into copy values (1104, '978-0132943260', null); 
insert into copy values (1105, '978-1950435098', null); 
insert into copy values (1106, '978-1950435098', null); 
insert into copy values (1107, '978-1950435098', null); 
insert into copy values (1108, '978-1950435098', null); 
insert into copy values (1109, '978-0870716065', null); 
insert into copy values (1110, '978-0870716065', null); 
insert into copy values (1111, '979-8749522310', null); 
insert into copy values (1112, '978-0375810886', null); 
insert into copy values (1113, '978-0143127741', null); 
insert into copy values (1114, '978-0321455369', null); 
insert into copy values (1115, '978-0321486813', null); 

insert into MEMBER values (330, 'Anna', null, 'Green', 'Broad', 'Cookeville', 'TN', 4, 38501, 9311234567, 'annagreen@tntech.edu', '2022-08-08'); 
insert into MEMBER values (331, 'Ben', 'Leo', 'Brown', 'Broad', 'Cookeville', 'TN', 124, 38501, 9312023030, 'benlbrown@tntech.edu', '2022-10-21'); 
insert into MEMBER values (332, 'Paul', null, 'Smith', 'Spring', 'Cookeville', 'TN', 23, 38506, 9313321314, 'paulsmith@tntech.edu', '2023-03-11'); 
insert into MEMBER values (333, 'Evan', 'David', 'Bailey', 'Jefferson', 'Cookeville', 'TN', 901, 38501, 9311234567, 'annagreen@tntech.edu', '2022-08-08'); 
insert into MEMBER values (334, 'Keith', 'Logan', 'Bailey', 'Jefferson', 'Cookeville', 'TN', 901, 38501, 9311234567, null, '2024-12-29'); 

insert into BORROW values (330, 1111, '2022-08-25 10:10:01', null, 0, null);
insert into BORROW values (331, 1105, '2022-09-03 17:56', null, 0, null);
insert into BORROW values (330, 1112, '2022-06-01 9:05:00', '2022-06-01 11:36:00', 0, null);
insert into BORROW values (331, 1105, '2022-08-15 12:07:13', '2022-08-25 18:30:30', 0, null);
insert into BORROW values (332, 1114, '2022-09-03 8:01:48', null, 0, null);
insert into BORROW values (333, 1113, '2022-08-01 11:31:24', null, 2, null);