create database ifn582;

use ifn582;

create table users (
	id INT NOT NULL AUTO_INCREMENT UNIQUE,    
	username VARCHAR(50) NOT null unique, -- username   
	firstname varchar(255) not null,
    surname varchar(255) not null,
    password varchar(255) not null,
    email varchar(255) not null unique,
    phone varchar(20) not null,
    user_type int not null default 0,
	primary key (id)
);

create table login_record(
    id INT NOT NULL AUTO_INCREMENT UNIQUE,
    user_id INT,
    login_time datetime,
    logout_time datetime,
    primary key (id),
    FOREIGN KEY (user_id) references users(id)
); -- semicolon was missing 


create table product (
	id varchar(255) not null UNIQUE, -- varchar value changed to 255 instead of 10, so that it matches with the table order.
    name varchar(255) not null,
    description varchar(255) not null,
	price DECIMAL(10,2) not null,
	quantity int not null,
	category varchar(100) not null,
    keyword varchar(20) not null,
	prescription varchar(255) not null,
    img1 varchar(255) not null,
    img2 varchar(255) not null,
    img3 varchar(255) not null,
    primary key (id)
);

create table orders (
	id INT AUTO_INCREMENT not null,
    user_id int,
    product_id varchar(255),
    amount DECIMAL(10,2),
	order_date DATETIME,
    delivery_type int default 0,
    address varchar(255) not null,
    payment_type int default 0,
	order_status int default 0,
    customer_name VARCHAR(100),
    customer_email VARCHAR(100),
    customer_phone VARCHAR(20),
    primary key (id),
    FOREIGN KEY (user_id) REFERENCES users(id),
	FOREIGN KEY (product_id) REFERENCES product(id) 
);



