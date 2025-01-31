create database if not exists library;
use library;

/* TRIGGER TO ADD DETAILS OF CARD HOLDER IN CARD DETAILS TABLE */
delimiter //
CREATE TRIGGER add_name_has_card_candidates
AFTER INSERT                                                
ON CUSTOMER_DETAILS FOR EACH ROW
begin
IF new.customer_id not in (select customer_id from library_card_details) and new.has_card = "YES" then 
insert into library_card_details(customer_id, name)
values(new.customer_id,new.name);
end if;
end ;
//
delimiter ;

/* TRIGGER TO ADD DONATED BOOKS IN BOOKS SECTION */
delimiter //
CREATE TRIGGER add_donated_books
BEFORE INSERT 
on DONATE_BOOKS FOR EACH ROW
begin
DECLARE code int;
SET code = FLOOR(101 + (RAND() * (999 - 101))) ;
INSERT into books values(code,new.book_name,new.book_condition);
end;
//
delimiter ;

/* DAILY LOG TABLE */
CREATE TABLE daily_log
(customer_id varchar(50),
entry_time datetime,
exit_time datetime);

/* PASSWORD TABLE */
CREATE TABLE password_table
(customer_id varchar(100),
user_password varchar(50));

/* CUSTOMER DETAILS */
CREATE TABLE CUSTOMER_DETAILS
(customer_id varchar(50) PRIMARY KEY,
name varchar(100) Not Null,
age int check (age > 0 and age < 200),
phone Bigint unique,
address varchar(100),
gmail_id varchar(100),
has_card varchar(10) DEFAULT 'No');

/* LIBRARY CARD */
CREATE TABLE LIBRARY_CARD_DETAILS
(customer_id varchar(100) UNIQUE,
library_card_id varchar(100) PRIMARY KEY,
name varchar(100) NOT NULL,
issue_date date,
valid_till date,
FOREIGN KEY (customer_id) REFERENCES CUSTOMER_DETAILS(customer_id)
ON DELETE CASCADE
ON UPDATE CASCADE);

/* PAYMENTS LOG */
CREATE TABLE PAYMENTS
(customer_id varchar(50) NOT NULL,
name varchar(100) NOT NULL,
amount float check (amount != 0),
mode varchar(20),
CHECK (mode IN ('UPI','Cash')),
payment_type varchar(50) NOT NULL,
date_of_payment date NOT NULL);

/*REQUESTED BOOKS*/
create table requested_book(
book_name varchar(100),
author_name varchar(100),
year_of_publication date,
date_of_request datetime,
expected_arrival datetime);

/* TABLE OCCUPIED */
CREATE TABLE TABLE_OCCUPIED
(table_no int,
table_status VARCHAR(20),
check(table_status in ("occupied","un-occupied")), 
FOREIGN KEY(table_no) REFERENCES TABLE_DETAILS(table_no)
ON DELETE CASCADE
ON UPDATE CASCADE);

/* BOOKS SECTION */
CREATE TABLE BOOKS
(book_id int NOT NULL,
book_name varchar(100) NOT NULL PRIMARY KEY,
book_author varchar(100) not null,
year_of_publication INT,
book_condition varchar(10),
book_niche varchar(100));

/* BOOK INSERT */
INSERT INTO BOOKS (book_id, book_name, book_author, year_of_publication, book_condition, book_niche)
VALUES
(921, 'To Kill a Mockingbird', 'Harper Lee', 1960, 'Excellent', 'Classic Literature'),
(734, '1984', 'George Orwell', 1949, 'Good', 'Classic Literature'),
(845, 'Pride and Prejudice', 'Jane Austen', 1813, 'Poor', 'Classic Literature'),
(214, 'The Great Gatsby', 'F. Scott Fitzgerald', 1925, 'Excellent', 'Classic Literature'),
(320, 'Moby-Dick', 'Herman Melville', 1851, 'Good', 'Classic Literature'),
(457, 'War and Peace', 'Leo Tolstoy', 1869, 'Poor', 'Classic Literature'),
(565, 'Jane Eyre', 'Charlotte Brontë', 1847, 'Excellent', 'Classic Literature'),
(678, 'Wuthering Heights', 'Emily Brontë', 1847, 'Good', 'Classic Literature');

INSERT INTO BOOKS (book_id, book_name, book_author, year_of_publication, book_condition, book_niche)
VALUES
(562, 'Dune', 'Frank Herbert', 1965, 'Excellent', 'Science Fiction and Fantasy'),
(738, 'Neuromancer', 'William Gibson', 1984, 'Good', 'Science Fiction and Fantasy'),
(485, 'A Game of Thrones', 'George R.R. Martin', 1996, 'Poor', 'Science Fiction and Fantasy'),
(620, 'The Left Hand of Darkness', 'Ursula K. Le Guin', 1969, 'Excellent', 'Science Fiction and Fantasy'),
(392, 'Snow Crash', 'Neal Stephenson', 1992, 'Good', 'Science Fiction and Fantasy'),
(755, 'The Hitchhiker\'s Guide to the Galaxy', 'Douglas Adams', 1979, 'Poor', 'Science Fiction and Fantasy'),
(239, 'Ender\'s Game', 'Orson Scott Card', 1985, 'Excellent', 'Science Fiction and Fantasy'),
(812, 'Good Omens', 'Neil Gaiman and Terry Pratchett', 1990, 'Good', 'Science Fiction and Fantasy');

INSERT INTO BOOKS (book_id, book_name, book_author, year_of_publication, book_condition, book_niche)
VALUES
(845, 'The Girl with the Dragon Tattoo', 'Stieg Larsson', 2005, 'Excellent', 'Mystery and Thriller'),
(973, 'Gone Girl', 'Gillian Flynn', 2012, 'Good', 'Mystery and Thriller'),
(634, 'The Da Vinci Code', 'Dan Brown', 2003, 'Poor', 'Mystery and Thriller'),
(278, 'And Then There Were None', 'Agatha Christie', 1939, 'Excellent', 'Mystery and Thriller'),
(321, 'The Silence of the Lambs', 'Thomas Harris', 1988, 'Good', 'Mystery and Thriller');

INSERT INTO BOOKS (book_id, book_name, book_author, year_of_publication, book_condition, book_niche)
VALUES
(412, 'All the Light We Cannot See', 'Anthony Doerr', 2014, 'Excellent', 'Historical Fiction'),
(578, 'The Book Thief', 'Markus Zusak', 2005, 'Good', 'Historical Fiction'),
(830, 'Wolf Hall', 'Hilary Mantel', 2009, 'Poor', 'Historical Fiction'),
(654, 'The Nightingale', 'Kristin Hannah', 2015, 'Excellent', 'Historical Fiction');

INSERT INTO BOOKS (book_id, book_name, book_author, year_of_publication, book_condition, book_niche)
VALUES
(234, 'Sapiens: A Brief History of Humankind', 'Yuval Noah Harari', 2011, 'Excellent', 'Non-Fiction'),
(567, 'The Immortal Life of Henrietta Lacks', 'Rebecca Skloot', 2010, 'Good', 'Non-Fiction'),
(891, 'Educated', 'Tara Westover', 2018, 'Poor', 'Non-Fiction'),
(101, 'Born a Crime', 'Trevor Noah', 2016, 'Excellent', 'Non-Fiction'),
(312, 'Quiet: The Power of Introverts in a World That Can\'t Stop Talking', 'Susan Cain', 2012, 'Good', 'Non-Fiction'),
(425, 'The Glass Castle', 'Jeannette Walls', 2005, 'Poor', 'Non-Fiction'),
(538, 'Bossypants', 'Tina Fey', 2011, 'Excellent', 'Non-Fiction'),
(649, 'I Know Why the Caged Bird Sings', 'Maya Angelou', 1969, 'Good', 'Non-Fiction'),
(754, 'Steve Jobs', 'Walter Isaacson', 2011, 'Poor', 'Non-Fiction'),
(863, 'Man\'s Search for Meaning', 'Viktor E. Frankl', 1946, 'Excellent', 'Non-Fiction');

INSERT INTO BOOKS (book_id, book_name, book_author, year_of_publication, book_condition, book_niche)
VALUES
(265, 'The Alchemist', 'Paulo Coelho', 1988, 'Good', 'Philosophy and Self Help'),
(378, 'The Road Less Traveled', 'M. Scott Peck', 1978, 'Poor', 'Philosophy and Self Help');

INSERT INTO BOOKS (book_id, book_name, book_author, year_of_publication, book_condition, book_niche)
VALUES
(489, 'The Waste Land', 'T.S. Eliot', 1922, 'Excellent', 'Poetry'),
(592, 'Milk and Honey', 'Rupi Kaur', 2014, 'Good', 'Poetry'),
(707, 'Leaves of Grass', 'Walt Whitman', 1855, 'Poor', 'Poetry'),
(813, 'Selected Poems', 'Langston Hughes', 1959, 'Excellent', 'Poetry');

/* BOOKS ISSUED */
CREATE TABLE BOOK_ISSUED
(customer_id varchar(50) NOT NULL,
issue_id varchar(50) NOT NULL,
book_id int NOT NULL,
book_name varchar(100) NOT NULL,
date_issued date,
return_date date,
due_days int DEFAULT 0,
penalty int DEFAULT 0);

/* BOOKS OCCUPIED */
CREATE TABLE BOOK_OCCUPIED
(book_id int NOT NULL,
book_name varchar(100) NOT NULL PRIMARY KEY,
customer_id varchar(100) NOT NULL,
time_taken datetime,
time_returned datetime);

/* DONATE BOOKS */
CREATE TABLE DONATE_BOOKS
(book_name varchar(100),
book_author varchar(100),
year_of_publication INT,
name_of_donor varchar(100),
book_condition varchar(10),
date_of_donation date);

/* TABLE OCCUPANCY */
CREATE TABLE TABLE_OCCUPANCY
(table_no int PRIMARY KEY,
table_occupancy varchar(50));

/* TABLE INSERT */
INSERT INTO TABLE_OCCUPANCY (table_no, table_occupancy)
VALUES 
('001', 'occupied'),
('002', 'un-occupied'),
('003', 'occupied'),
('004', 'un-occupied'),
('005', 'occupied'),
('006', 'un-occupied'),
('007', 'occupied'),
('008', 'un-occupied'),
('009', 'occupied'),
('010', 'un-occupied'),
('011', 'occupied'),
('012', 'un-occupied'),
('013', 'occupied'),
('014', 'un-occupied'),
('015', 'occupied'),
('016', 'un-occupied'),
('017', 'occupied'),
('018', 'un-occupied'),
('019', 'occupied'),
('020', 'un-occupied'),
('021', 'occupied'),
('022', 'un-occupied'),
('023', 'occupied'),
('024', 'un-occupied'),
('025', 'occupied'),
('026', 'un-occupied'),
('027', 'occupied'),
('028', 'un-occupied'),
('029', 'occupied'),
('030', 'un-occupied'),
('031', 'occupied'),
('032', 'un-occupied'),
('033', 'occupied'),
('034', 'un-occupied'),
('035', 'occupied'),
('036', 'un-occupied'),
('037', 'occupied'),
('038', 'un-occupied'),
('039', 'occupied'),
('040', 'un-occupied'),
('041', 'occupied'),
('042', 'un-occupied'),
('043', 'occupied'),
('044', 'un-occupied'),
('045', 'occupied'),
('046', 'un-occupied'),
('047', 'occupied'),
('048', 'un-occupied'),
('049', 'occupied'),
('050', 'un-occupied');

/* REQUESTED BOOK */
create table requested_books(
book_name varchar(100),
author_name varchar(50),
year_of_publication varchar(10),
name_of_requester varchar(50),
id_of_requester varchar(50),
requested_date datetime);





