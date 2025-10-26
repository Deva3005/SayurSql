-- CREATE DATABASE BookStore_remastered;

-- show DATABASES;

-- use BookStore_remastered;

-- show tables;

-- CREATE Table Customers (
--     id int PRIMARY KEY AUTO_INCREMENT,
--     name VARCHAR(50),
--     email VARCHAR(50) UNIQUE,
--     city VARCHAR(25)
-- );

-- CREATE TABLE Books (
--     id INT PRIMARY KEY AUTO_INCREMENT,
--     title VARCHAR(100),
--     author VARCHAR(50),
--     price DECIMAL(5,2),
--     quantity INT
-- );


-- CREATE TABLE Sales (
--     id INT PRIMARY KEY AUTO_INCREMENT,
--     bookid INT NOT NULL,
--     customerid INT NOT NULL,
--     quantity_sold INT NOT NULL,
--     sales_date DATE NOT NULL,
-- );

-- alter table `Sales` add constraint fkcust1 FOREIGN KEY(customerid) REFERENCES `Customers`(id) on delete CASCADE on update CASCADE;
-- alter table `Sales` add constraint fkbook1 FOREIGN KEY(bookid) REFERENCES `Books`(id) on delete CASCADE on update CASCADE;

-- select * from `Customers`;

-- select * from `Sales`;

-- INSERT INTO `Sales` (bookid,customerid,quantity_sold,sales_date) VALUES ()

-- # Restock
-- update `Books` SET quantity=30
-- WHERE quantity<0

-- SELECT * FROM `Books` where quantity <0;


-- select s.sales_date,b.title,b.author,b.price,s.quantity_sold,c.name,c.email,c.city
--     from `Sales` as s 
--     JOIN `Books` as b 
--         on s.bookid = b.id
--     JOIN `Customers` as c
--         on s.customerid = c.id
--     limit 10 OFFSET 0; 


-- select * from `Customers`;


-- # PURCHASE TABLE FOR CUSTOMER
-- SELECT
--         s.sales_date,
--         c.name,
--         -- c.email,
--         c.city,
--         -- s.bookid,
--         b.title,
--         CONCAT("x ",s.quantity_sold),
--         CONCAT("$ ",b.price),
--         CONCAT("$ ",b.price*s.quantity_sold) as total 
--     from `Customers` as c
--     LEFT JOIN `Sales` as s ON c.id=s.customerid
--     LEFT JOIN `Books` as b on b.id=s.bookid
--     -- GROUP BY city
--     where c.id=4
--     ORDER BY s.sales_date desc
--     LIMIT 10 OFFSET 10;

-- # MOST VALUBLE CITY
-- SELECT 
--         -- c.id,c.name,c.email,
--         c.city,
--         -- s.sales_date,s.bookid,
--         sum(s.quantity_sold),
--         -- b.title,b.price,
--         sum(b.price*s.quantity_sold) as total 
--     from `Customers` as c
--     LEFT JOIN `Sales` as s ON c.id=s.customerid
--     LEFT JOIN `Books` as b on b.id=s.bookid
--     GROUP BY city
--     ORDER BY total desc;

-- # MOST VALUBLE CUSTOMER
-- SELECT 
--         c.id,c.name,c.email,
--         c.city,
--         -- s.sales_date,s.bookid,
--         sum(s.quantity_sold),
--         -- b.title,b.price,
--         sum(b.price*s.quantity_sold) as total 
--     from `Customers` as c
--     LEFT JOIN `Sales` as s ON c.id=s.customerid
--     LEFT JOIN `Books` as b on b.id=s.bookid
--     GROUP BY c.id
--     ORDER BY total desc
--     LIMIT 1;

--     SELECT * from `Books` where quantity<0;

--     update `Books` set quantity = 30
--     where quantity <= 0;


select * from `Customers`;
update `Customers`
set name = 'Ganesh Varadha', email="ganesh@example.com"
where id=3;

select * from `Sales` where customerid=3;

delete from `Sales` where customerid=3;