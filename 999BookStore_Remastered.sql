CREATE DATABASE BookStore_remastered;

show DATABASES;

use BookStore_remastered;

show tables;

CREATE Table Customers (
    id int PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    email VARCHAR(50) UNIQUE,
    city VARCHAR(25)
);

CREATE TABLE Books (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(100),
    author VARCHAR(50),
    price DECIMAL(5,2),
    quantity INT
);


CREATE TABLE Sales (
    id INT PRIMARY KEY AUTO_INCREMENT,
    bookid INT NOT NULL,
    customerid INT NOT NULL,
    quantity_sold INT NOT NULL,
    sales_date DATE NOT NULL,
);

alter table `Sales` add constraint fkcust1 FOREIGN KEY(customerid) REFERENCES `Customers`(id) on delete CASCADE on update CASCADE;
alter table `Sales` add constraint fkbook1 FOREIGN KEY(bookid) REFERENCES `Books`(id) on delete CASCADE on update CASCADE;

select * from `Customers`;

select * from `Sales`;

INSERT INTO `Sales` (bookid,customerid,quantity_sold,sales_date) VALUES ()