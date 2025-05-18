create database ifn582;

use ifn582;

create table Users (
	id int not null AUTO_INCREMENT UNIQUE,    
	username varchar(50) not null unique,  
	firstname varchar(255) not null,
    surname varchar(255) not null,
    password varchar(255) not null,
    email varchar(255) not null unique,
    phone varchar(20) not null,
	primary key (id)
);

create table Address (
	id int not null AUTO_INCREMENT UNIQUE,
    street varchar(255) not null,
    suburb varchar(255) not null,
    postcode char(4) not null,
    state varchar(3) not null,
    primary key (id)
);

create table Product (
	id int not null AUTO_INCREMENT UNIQUE,
    title varchar(255) not null,
    description varchar(255) not null,
    category varchar(100) not null,
    stock int not null,
    price float not null,
    img varchar(255) not null,
    primary key (id)
);

create table ShoppingCart (
	id int not null,
    productId int not null,
    userId int not null,
    qty int not null,
    total_price float not null,
    primary key (id),
    foreign key (productId) references Product(id),
    foreign key (userId) references Users(id)
);

create table Checkout (
	id int not null AUTO_INCREMENT unique,
    shoppingcart_id int not null,
    address_id int not null,
    order_number int not null unique,
    order_time datetime not null,
    order_total_price float not null,
    primary key (id),
    foreign key (shoppingcart_id) references ShoppingCart(id),
	foreign key (address_id) references Address(id)
);


