
-- -------------------------------------------------------------------
-- 2023-02-28 : adding partitions to historical_data
-- -------------------------------------------------------------------
-- -------------------------------------------------------------------
-- creating schema opa
-- -------------------------------------------------------------------

show databases;
create database
if not exists opa;

-- -------------------------------------------------------------------
-- creating specific user datascientest
-- -------------------------------------------------------------------
create user
if not exists 'datascientest'@'%' identified by 'temp123';
grant all privileges on opa.* to 'datascientest'@'%' with grant option;
grant all privileges on opa.* to 'root'@'%' with grant option;
flush privileges;
select host
  , user
from mysql.user;

-- -------------------------------------------------------------------
-- connection to opa
-- -------------------------------------------------------------------
use opa;

-- -------------------------------------------------------------------
-- creating tables historical_klines, stream_klines, symbol_interval
-- -------------------------------------------------------------------
drop table if exists historical_klines ;
drop table if exists stream_klines ;
drop table if exists symbol_interval ;
drop table if exists api_users ;
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
    
/* 
 insert into symbol_interval values (2, 'BTCUSDT', '15m', now(), now(), 0, 0) ;
 insert into symbol_interval values (3, 'BTCUSDT', '5m', now(), now(), 0, 0) ;
 insert into symbol_interval values (4, 'BTCUSDT', '1m', now(), now(), 0, 0) ;
 insert into symbol_interval values (5, 'BTCUSDT', '1s', now(), now(), 0, 0) ;
 insert into symbol_interval values (6, 'ETHUSDT', '1m', now(), now(), 0, 0) ;
 insert into symbol_interval values (7, 'XRPUSDT', '1m', now(), now(), 0, 0) ;
 */
-- ------------------------------------------------------------------- 
drop table if exists historical_klines ;
create table if not exists historical_klines
    (
        id_symint int not null
      , open_time bigint not null
      , open_price float not null
      , high_price float not null
      , low_price float not null
      , close_price float not null
      , volume float not null
      , close_time bigint not null
      , quote_asset_volume float not null
      , number_of_trades float not null
      , taker_buy_base_asset_volume float not null
      , taker_buy_quote_asset_volume float not null
      , primary key(id_symint, open_time)
    )
  PARTITION BY RANGE  (id_symint) (
  PARTITION P_0 values less than (1),
  PARTITION P_1 values less than (2),
  PARTITION P_2 VALUES less than (3),
  PARTITION P_3 VALUES less than (4),
  PARTITION P_4 VALUES less than (5),
  PARTITION P_5 VALUES less than (6),
  PARTITION P_DEFAULT values less than  (100)
);
-- ------------------------------------------------------------------- 
drop table if exists stream_klines ;
create table if not exists stream_klines
    (
      /*  id_symint        int not null 
      , event_type       varchar(16) not null 
      ,*/ symbol           varchar(16) not null
      , interval_symbol         varchar(16) not null
      , event_time       bigint not null
      , kline_start_time bigint not null
      , kline_close_time bigint not null
      , first_trade_id   bigint not null
      , last_trade_id    bigint not null
      , open_price float not null
      , close_price float not null
      , high_price float not null
      , low_price float not null
      , base_asset_volume float not null
      , number_of_trades float not null
      , is_this_kline_closed boolean not null
      , quote_asset_volume float not null
      , taker_buy_base_asset_volume float not null
      , taker_buy_quote_asset_volume float not null
      , primary key(symbol, interval_symbol,kline_start_time)
        /*
        , foreign key(id_symint) references symbol_interval(id_symint)*/
    )
    engine = memory;
-- -------------------------------------------------------------------
-- creating and populate api_users table
-- -------------------------------------------------------------------
drop table if exists api_users ;
create table api_users
    (
        id_api_users int not null 
      , name         varchar(30) not null
      , lastname     varchar(30) not null
      , date_insert timestamp not null
      , date_update timestamp not null
      , last_login timestamp null
      , is_active    boolean not null
      , login        varchar(30) not null
      , password     varchar(30) not null
      , validity_day int not null
      , primary key(id_api_users)
    )
    engine = innodb default charset = utf8mb4 default collate = utf8mb4_0900_ai_ci;
insert
into api_users values
    (
        1
      , 'ilham'
      , 'noumir'
      , now()
      , now()
      , null
      , 1
      , 'hennaji'
      , 'temp123'
      , 180
    ) ;
insert
into api_users values
    (
        2
      , 'hamza'
      , 'ennaji'
      , now()
      , now()
      , null
      , 1
      , 'hennaji'
      , 'temp123'
      , 180
    ) ;
insert
into api_users values
    (
        3
      , 'loic'
      , 'montagnac'
      , now()
      , now()
      , null
      , 1
      , 'lmontagnac'
      , 'temp123'
      , 180
    ) ;
insert
into api_users values
    (
        4
      , 'souhila'
      , 'lebib'
      , now()
      , now()
      , null
      , 1
      , 'slebib'
      , 'temp123'
      , 180
    ) ;
insert
into api_users values
    (
        5
      , 'simon'
      , 'cariou'
      , now()
      , now()
      , null
      , 1
      , 'scariou'
      , 'temp123'
      , 180
    ) ;

