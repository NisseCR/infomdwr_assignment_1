drop table if exists customer;
drop table if exists branch;
drop table if exists account;
drop table if exists loan;
drop table if exists employee;


-- Create tables.
create table customer (
    customer_id integer not null primary key autoincrement,
    street varchar(20) not null,
    house_number varchar(20) not null, -- korea exists
    city varchar(20) not null,
    country varchar(20) not null,
    first_name varchar(20) not null,
    surname varchar(20) not null
);

create table branch (
    branch_id integer not null primary key autoincrement, -- this is the key, not name, so change loan and employee. we smort
    branch_name varchar(20) not null unique,
    street varchar(20) not null,
    building_number varchar(20) not null, -- korea exists
    city varchar(20) not null,
    phone_number varchar(20) unique -- leading zero!! and not not null because new branch setup b4 contract or elders have only physical place.
);

create table account (
    account_id integer not null primary key autoincrement,
    customer_id integer not null,
    balance float not null,
    branch_id integer not null,
    foreign key (customer_id) references customer,
    foreign key (branch_id) references branch
);

create table loan (
    loan_id integer not null primary key autoincrement,
    branch_id integer not null,
    customer_id integer not null,
    amount float not null,
    currency varchar(20),
    foreign key (branch_id) references branch,
    foreign key (customer_id) references customer
);

create table employee (
    employee_id integer not null primary key autoincrement,
    branch_id integer not null,
    first_name varchar(20) not null,
    surname varchar(20) not null,
    salary float not null, --include volunteers or not being paid ppl
    role varchar(20) not null,
    foreign key (branch_id) references branch,
    check (salary >= 0) -- imagine paying to work
);

-- Seed database.
insert into customer (street, house_number, city, country, first_name, surname)
values ("Via delle Fondameta", 1, "Vatican", "Vatican City", "Innocensius", "II"),
       ("Jeungsan-ro, Mapo-gu", 87, "Seoul", "South-Korea", "Kim", "Impossible"),
       ("Broadway", 219, "New York", "United States", "Orpheus", "II"),
       ("Broadway", 219, "New York", "United States", "Eurydice", "II");

