
from termcolor import colored 
import mysql.connector

class SqlAction:
    conn = mysql.connector.connect(
                user ='datascientest',
                passwd ='temp123',
                host ='127.0.0.1',
                port ="3306",
                database ="opa"
            )  
    curr = conn.cursor(dictionary=True) 
  
#############################################################################################################
#############################################################################################################
#############################################################################################################

    def __init__(self):
        pass

    def sql_retry(self,retry=5):
        pass
#############################################################################################################
# OPA SYMBOL INTERVAL FUNCTIONS
#############################################################################################################
    def get_symbol_interval(self) :
        try : 
            query = "select *  from opa.symbol_interval"
            self.curr.execute(query)
            symint = [item for item in self.curr.fetchall()]
            return symint
            print(colored(symint,"red"))
        except :
            print(colored("get_symbol_interval : unable to do action","red"))
            raise

    def update_symbol_interval_starttime(self, id_symint, starttime) :        
        try : 
            query = "update opa.symbol_interval set  starttime = {0}, date_update = now() where id_symint = {1}".format(starttime,id_symint)
            self.curr.execute(query)
            self.conn.commit()  
        except :
            print(colored("update_symbol_interval : unable to do action","red"))

    def update_symbol_interval_endtime(self, id_symint, endtime) :        
        try : 
            query = "update opa.symbol_interval set  endtime = {0}, date_update = now() where id_symint = {1}".format(endtime,id_symint)
            self.curr.execute(query)
            self.conn.commit()  
        except :
            print(colored("update_symbol_interval : unable to do action","red"))
            raise
#############################################################################################################
# OPA HISTORICAL KLINES FUNCTIONS
#############################################################################################################
    def store_historical_klines(self, id_symint, val) :
        try :                     
            
            query = "replace into opa.historical_klines  (id_symint, open_time, open_price, high_price, low_price, close_price, \
            volume, close_time, quote_asset_volume, number_of_trades, taker_buy_base_asset_volume, taker_buy_quote_asset_volume )\
            values ({}, %s , %s , %s , %s , %s , %s , %s , %s , %s , %s, %s)".format(id_symint)
            self.curr.executemany(query,val)
            self.conn.commit()
            print(self.curr.rowcount, "was inserted.")
            return 
        except :
            print(colored("store_historical_klines : unable to do action","red"))
            raise

        
    def retrieve_historical_klines(self, id_symint) :
        try : 
            query = "select *  from opa.historical_klines where id_symint={0} order by open_time ".format(id_symint)
            self.curr.execute(query)
            data = self.curr.fetchall()
            # print(colored(data,"red"))
            return data
        except :
            print(colored("get_symbol_interval : unable to do action","red"))
            raise

#############################################################################################################
# OPA STREAM KLINES FUNCTIONS
#############################################################################################################
    def store_stream_klines(self, val) :
        try :  
            columns_def = {
                            "t":"kline_start_time",
                            "T":"kline_close_time",
                            "i":"interval_symbol",
                            "s":"symbol",
                            "f":"first_trade_id",
                            "L":"last_trade_id",
                            "o":"open_price",
                            "c":"close_price",
                            "h":"high_price",
                            "l":"low_price",
                            "v":"base_asset_volume",
                            "n":"number_of_trades",
                            "x":"is_this_kline_closed",
                            "q":"quote_asset_volume",
                            "V":"taker_buy_base_asset_volume",
                            "Q":"taker_buy_quote_asset_volume",
                            "B":"ignore"
			                }

            for k, v in columns_def.items() :
                val[v]=val.pop(k)

            varlist = list(val.values())
            varlist = varlist[:-1]
            
            keylist = list(val.keys())
            keylist = keylist[:-1]
            columns_string = ", ".join(keylist)
            print(colored(varlist,"red"))
            print(colored(keylist,"yellow"))

            query = "replace into opa.stream_klines (  {} )\
            values ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(columns_string)
            print(colored(query,"green"))
            self.curr.execute(query,varlist)
            self.conn.commit()
            print("1 row was inserted.")
            return 
        except :
            print(colored("store_historical_klines : unable to do action","red"))
            raise


    def purge_stream_klines(self) :
        try : 
            query = "delete \
                    from opa.stream_klines a \
                    where exists \
                        (select 1  \
                            from(select symbol \
                                    , interval_symbol \
                                    , kline_start_time \
                                    , rank() over(partition by symbol, interval_symbol order by kline_start_time desc) my_rank \
                                    from stream_klines) abc \
                            where 1 = 1 \
                                and my_rank = 1000 \
                                and abc.symbol = a.symbol \
                                and abc.interval_symbol = a.interval_symbol \
                                and abc.kline_start_time > a.kline_start_time)"
            # print(query)
            self.curr.execute(query)
            
            print("Purge terminated")
            return 0
        except :
            print(colored("purge_stream_klines : unable to do action","red"))
            raise



        