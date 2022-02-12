# **postgres refrence commands to remember and setup test db environment**

**commands on psql shell**
- create database databasename;  to create database

- \c databasename; to choose the database created

- \l to show databases

- \dt to show tables

- ctrl+l to clear screen

- sample query to create table 
```
create table accounts (
	user_id serial PRIMARY KEY,
	username VARCHAR ( 50 ) UNIQUE NOT NULL,
	password VARCHAR ( 50 ) NOT NULL,
	email VARCHAR ( 255 ) UNIQUE NOT NULL,
	created_on TIMESTAMP NOT NULL,
    last_login TIMESTAMP 
);
```
- smaple query to insert data into table 
```
insert into accounts values(1,'shivamsherkar','abc123','shivam@mail.com','2020-06-22 19:10:25-07','2020-06-22 19:10:25-07');
```

- name appear before the hashtag in psql shell is the database name which is in use

- other refrence commands

### **start psql shell from the current ubuntu user**
sudo -u postgres psql 

### **run the fastapi application**
uvicorn main:app --reload

### **to get the modules used and install them**
- pip freeze > requirements.txt 
- pip install -r requirements.txt

### **set password for postgres database**
- ALTER USER user_name WITH PASSWORD 'new_password';

### **installing postgres**
install psycopg2-binary \
install psycopg2-binary \
sudo apt install build-essential