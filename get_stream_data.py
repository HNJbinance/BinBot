#!/usr/bin/env python
import logging
import modules.sql_properties as sql 
from binance.lib.utils import config_logging
from binance.websocket.spot.websocket_stream import SpotWebsocketStreamClient

config_logging(logging, logging.DEBUG)
sql = sql.SqlAction()

def message_handler(_, message):
    logging.info(message)


my_client = SpotWebsocketStreamClient(on_message=message_handler, is_combined=True)
columns_def = {
			"e":"event_type",
			"E":"event_time",
			"s":"symbol",
			"k":"",
			"t":"kline_start_time",
			"T":"kline_close_time",
			"i":"interval",
			"f":"first_trade_id",
			"L":"last_trade_id",
			"o":"open_price",
			"c":"close_price",
			"h":"high_price",
			"l":"low_price",
			"v":"base_asset_volume",
			"n":"number_of_trades",
			"x":"is_this_kline_closed?",
			"q":"quote_asset_volume",
			"V":"taker_buy_base_asset_volume",
			"Q":"taker_buy_quote_asset_volume",
			"B":"ignore"
			}

symint = sql.get_symbol_interval()
# loop on every symbol/interval requested
for val in symint :    
    db_interval=val['interval_symbol']
    db_symbol = val['symbol'].lower()
    # subscribe ethusdt 3m kline
    my_client.kline(symbol=db_symbol, interval=db_interval)

