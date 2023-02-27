
from termcolor import colored 
import mysql.connector

class SqlAction:
    conn = mysql.connector.connect(
                user ='datascientest',
                passwd ='temp123',
                host ='52.51.116.43',
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

    def update_symbol_interval(self, id_symint, endtime) :        
        try : 
            query = "update opa.symbol_interval set  endtime = {0}, date_update = now() where id_symint = {1}".format(endtime,id_symint)
            self.curr.execute(query)
            self.conn.commit()  
        except :
            print(colored("update_symbol_interval : unable to do action","red"))
#############################################################################################################
# OPA HISTORICAL KLINES FUNCTIONS
#############################################################################################################
    def store_historical_klines(self, id_symint, val) :
        try :                     
            
            query = "insert into opa.historical_klines  (id_symint, open_time, open_price, high_price, low_price, close_price, \
            volume, close_time, quote_asset_volume, number_of_trades, taker_buy_base_asset_volume, taker_buy_quote_asset_volume )\
            values ({}, %s , %s , %s , %s , %s , %s , %s , %s , %s , %s, %s)".format(id_symint)
            self.curr.executemany(query,val)
            self.conn.commit()
            print(self.curr.rowcount, "was inserted.")
            return 
        except :
            print(colored("store_historical_klines : unable to do action","red"))
            raise

#############################################################################################################
# OPA STREAM KLINES FUNCTIONS
#############################################################################################################
    # def store_stream_klines(self, id_origin) :
    #     try : 
    #         query = "select id  from {0}".format(self.ad_table[id_origin])
    #         self.curr.execute(query)
    #         ids = [item[0] for item in self.curr.fetchall()]
    #         return ids
    #     except :
    #         print(colored("unable to do action","red"))

