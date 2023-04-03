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
-- -------------------------------------------------------------------
-- connection to opa
-- -------------------------------------------------------------------
use opa;
-- -------------------------------------------------------------------
-- creating tables historical_klines, stream_klines, symbol_interval
-- -------------------------------------------------------------------
drop table
if exists historical_klines ;
drop table
if exists stream_klines ;
drop table
-- -------------------------------------------------------------------
drop table
if exists historical_klines ;
create table
    if not exists historical_klines
    (
        symbol                      varchar(10) not null, 
        interval_symbol             varchar(4) not null, 
        open_time                    bigint not null ,
        open_price                   float not null ,
        high_price                   float not null ,
        low_price                    float not null ,
        close_price                  float not null ,
        volume                       float not null ,
        close_time                   bigint not null ,
        quote_asset_volume           float not null ,
        number_of_trades             float not null ,
        taker_buy_base_asset_volume  float not null ,
        taker_buy_quote_asset_volume float not null ,
        primary key(symbol, interval_symbol,open_time)
    );
-- -------------------------------------------------------------------
drop table
if exists stream_klines ;
create table
    if not exists stream_klines
    (
        
        symbol                       varchar(16) not null ,
        interval_symbol              varchar(16) not null ,
        event_time                   bigint not null,
        open_time                    bigint not null ,
        close_time                   bigint not null ,
        first_trade_id               bigint not null ,
        last_trade_id                bigint not null ,
        open_price                   float not null ,
        close_price                  float not null ,
        high_price                   float not null ,
        low_price                    float not null ,
        base_asset_volume            float not null ,
        number_of_trades             float not null ,
        is_this_kline_closed         boolean not null ,
        quote_asset_volume           float not null ,
        taker_buy_base_asset_volume  float not null ,
        taker_buy_quote_asset_volume float not null ,
        primary key(symbol, interval_symbol)
       
    );
