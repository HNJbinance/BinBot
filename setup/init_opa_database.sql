show databases;
create database if not exists opa;
########################################;
create user if not exists 'datascientest'@'%' identified by 'temp123';
grant all privileges on opa.* to 'datascientest'@'%' with grant option;
grant all privileges on opa.* to 'root'@'%' with grant option;
flush privileges;
select host
  , user
from mysql.user;
######################################## ;
use opa;
########################################;
drop table if exists historical_klines ;
drop table if exists stream_klines ;
drop table if exists symbol_interval ;
create table if not exists symbol_interval
    (
        id_symint       int not null
      , symbol          varchar(10) not null
      , interval_symbol varchar(4) not null
      , date_insert timestamp not null
      , date_update timestamp not null
      , starttime bigint not null
      , endtime   bigint not null
      , primary key(id_symint)
    ) ;
--
insert
into symbol_interval values
    (
        1
      , 'BTCUSDT'
      , '1h'
      , now()
      , now()
      , 0
      , 0
    ) ;
######################################## ;
drop table if exists historical_klines ;
create table if not exists historical_klines
    (
        id_symint int not null
      , opentime  bigint not null
      , open float not null
      , high float not null
      , low float not null
      , close float not null
      , volume float not null
      , closetime        bigint not null
      , quoteassetvolume float not null
      , numberoftrades float not null
      , takerbuybaseassetvolume float not null
      , takerbuyquotassetvolume float not null
      , primary key(id_symint, opentime)
      , foreign key(id_symint) references symbol_interval(id_symint)
    ) ;
######################################## ;
drop table if exists stream_klines ;
create table if not exists stream_klines
    (
        id_symint int not null
      , opentime  bigint not null
      , open float not null
      , high float not null
      , low float not null
      , close float not null
      , volume float not null
      , closetime        bigint not null
      , quoteassetvolume float not null
      , numberoftrades float not null
      , takerbuybaseassetvolume float not null
      , takerbuyquotassetvolume float not null
      , primary key(id_symint, opentime)
        /*
        , foreign key(id_symint) references symbol_interval(id_symint)*/
    )
    engine = memory;