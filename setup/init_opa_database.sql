
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

-- ------------------------------------------------------------------- 
drop table if exists historical_klines_v2 ;
create table if not exists historical_klines_v2
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
  PARTITION P_0 values less than (1),insert into opa.stream_klines (id_symint, event_time, kline_start_time,\
                 kline_close_time, interval_symbol, symbol, first_trade_id, last_trade_id, open_price, close_price, high_price,\
                     low_price, base_asset_volume, number_of_trades, is_this_kline_closed, quote_asset_volume, taker_buy_base_asset_volume, taker_buy_quote_asset_volume )\
            values 
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