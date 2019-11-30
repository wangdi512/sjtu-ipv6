create user zjc@'%' IDENTIFIED by 'zjc13120709021';
grant all privileges on *.* to 'zjc'@'%' identified by 'zjc13120709021';

create database dns;
use dns;
create table amallog(domain varchar(255),
						ip varchar(255),
						time varchar(255),
						srcip varchar(255));
create table log1(domain varchar(255),ip varchar(255),time varchar(255),srcip varchar(255));
create table location(domain varchar(255),country varchar(255),city varchar(255),latitude varchar(255),longitude varchar(255));
create table logcount(logtype varchar(255),totalnum varchar(255));
insert into logcount (logtype,totalnum) values ('log','0');
create table tongji (date varchar(255),id varchar(255),malcount varchar(255),logcount varchar(255));
create table systime (year int, month int, day int, hour int, minute int, second int);
create database smalldata;
use smalldata;
source /docker-entrypoint-initdb.d/sql/smalldata.sql;

-- GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '123456' WITH GRANT OPTION;
-- flush privileges;
