-- #create user flavio with password '';
-- #create database sige;


create table user_status(
    id serial primary key,
    status text not null
);
insert into user_status (status) values ('ativo');
insert into user_status (status) values ('inativo');
insert into user_status (status) values ('pendente');
select * from user_status;





create table users(
    id serial primary key,
    name varchar(25),
    email varchar(45) not null,
    password text not null,
    status_id integer REFERENCES user_status (id)
);
-- insert into users (name, email, password, status_id) values ('flavio', 'flavio@sige.com', 'senha', 1);
-- insert into users (name, email, password, status_id) values ('natalie', 'natalie@sige.com', 'senha', 1);
select * from users;


create table permission(
    id serial primary key,
    name text not null
);
insert into permission (name) values ('user');
insert into permission (name) values ('master');
select * from permission;



create table user_permission(
    permission_id integer REFERENCES permission (id) , 
    user_id integer REFERENCES users (id)          
);

select * from user_permission;


-- create table intern_record(
--     id serial primary key,
--     user_id integer REFERENCES users (id)
-- );
-- insert into intern_record (user_id) values (1);
-- select * from intern_record;

create table password_recovery(
    user_id integer REFERENCES users (id),
    code_id integer not null
);

-- select * from users inner join user_status on users.status_id =  user_status.id order by users.id;

create table company(
    id serial primary key,
    cnpj bigint not null,
    company_name varchar(45) not null,
    opening_date text not null,
    contact_email varchar(45) not null,
    zip_code varchar(100) not null,
    address varchar(100) not null,
    contact_phone varchar(45) not null,
    contact_person varchar(45),
    associated_since varchar(100) not null,
    associated_until varchar(100)
);