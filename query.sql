
create database apr01;
use apr01;

create table categories(
    category_id int primary key,
    category_name nvarchar(15)
);

create table users(
    user_id int auto_increment primary key,
    user_name varchar(30) unique not null,
    password varchar(30) not null
);

create table schedules(
    schedule_id int auto_increment primary key,
    user_id int not null,
    category_id int not null references categories.category_id,
    days date not null,
    schedule nvarchar(17) not null
);


set names cp932;
insert into categories values(1, '学校');
insert into categories values(2, '試験');
insert into categories values(3, '課題');
insert into categories values(4, '行事');
insert into categories values(5, '就活');
insert into categories values(6, 'アルバイト');
insert into categories values(7, '旅行');
