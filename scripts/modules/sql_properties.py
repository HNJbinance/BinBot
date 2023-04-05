
import mysql.connector
import os
import pandas as pd


class SqlAction:
    try : 
        print("docker compose connection...")
        conn = mysql.connector.connect(
                    
                    user ='datascientest',
                    passwd ='temp123',                
                    # host ='172.17.0.1',
                    # port ="3306",
                    host = os.environ.get("DB_HOST"),
                    port =os.environ.get("DB_PORT"),
                    database ="opa"
                )  
        curr = conn.cursor(dictionary=True) 
    except : 
        try :             
            print("docker connection...")
            conn = mysql.connector.connect(
                        user ='datascientest',
                        passwd ='temp123',                     
                        host ='172.17.0.1',      
                        port ="3306",
                        # host = os.environ.get("DB_HOST"),
                        # port =os.environ.get("DB_PORT"),
                        database ="opa"
                    )  
            curr = conn.cursor(dictionary=True) 
        except : 
            print("Direct connection...")
            conn = mysql.connector.connect(
                        user ='datascientest',
                        passwd ='temp123',     
                        host ='ec2-52-210-133-120.eu-west-1.compute.amazonaws.com',
                        port ="3306",
                        # host = os.environ.get("DB_HOST"),
                        # port =os.environ.get("DB_PORT"),
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
# OPA HISTORICAL KLINES FUNCTIONS
#############################################################################################################
    def store_historical_klines(self,symbol_,interval_, val) :
        try :                     
            
            query = "replace into opa.historical_klines  (symbol,interval_symbol, open_time, open_price, high_price, low_price, close_price, \
            volume, close_time, quote_asset_volume, number_of_trades, taker_buy_base_asset_volume, taker_buy_quote_asset_volume )\
            values ('{}', '{}', %s , %s , %s , %s , %s , %s , %s , %s , %s , %s, %s)".format(symbol_,interval_)
            print(query)
            self.curr.executemany(query,val)
            self.conn.commit()
            print(self.curr.rowcount, "was inserted.")
        except :
            print("store_historical_klines : unable to do action")
            raise

        
    def retrieve_historical_klines(self) :
        try : 
            query = "select *  from opa.historical_klines order by open_time asc limit 90000"
            self.curr.execute(query)
            data = self.curr.fetchall()
            # print(data)
            return data
        except :
            print("retrieve_historical_klines : unable to do action")
            raise


    def retrieve_last_open_time(self) :
        try : 
            query = "select ifnull(max(open_time),0) open_time  from opa.historical_klines "
            self.curr.execute(query)
            data = self.curr.fetchall()
            # print(data)
            return data
        except :
            print("retrieve_last_open_time : unable to do action")
            raise

    def retrieve_historical_klines_dataframe(self) :
        try : 
            query = "select *  from opa.historical_klines order by open_time asc limit 90000"
            self.curr.execute(query)
            data_raw = self.curr.fetchall()
            # print(data)
            data = pd.DataFrame()
            data = data.append(data_raw, ignore_index=True)
            #Défine column_name we will add to features
            lag_columns = ['open_price', 'high_price', 'low_price', 'close_price', 'volume', 
                        'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 
                        'taker_buy_quote_asset_volume']
            #define number time we will add the lags columns to features
            lag_count = 2
            #adding data
            for col in lag_columns:
                for lag in range(1, lag_count + 1):
                    data[f'{col}_lag-{lag}'] = data[col].shift(lag)
            data['next_close_price'] = data['close_price'].shift(-1)
            data = data.dropna()
            feats = data.drop(['open_time','close_time','next_close_price','symbol', 'interval_symbol'], axis=1)
            target = data['next_close_price']

            return feats,target
        except :
            print("retrieve_historical_klines : unable to do action")
            raise
#############################################################################################################
# OPA STREAM KLINES FUNCTIONS
#############################################################################################################
    def store_stream_klines(self, val) :
        try :  
            columns_def = {   
                            "t":"open_time",
                            "T":"close_time",
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
            print(varlist)
            print(keylist)

            query = "replace into opa.stream_klines (  {} )\
            values ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(columns_string)
            print(query)
            self.curr.execute(query,varlist)
            self.conn.commit()
            print("1 row was inserted.")
            return 
        except :
            print("store_stream_klines : unable to do action")
            raise

    def retrieve_stream_price_and_next_hour(self) :
        try : 
            query = 'select    close_price ,    date_format( date_add(from_unixtime( \
                substring( event_time, 1 , char_length( event_time) - 3) \
                ) ,interval 1 hour) , "%Y-%m-%d %H:00:00") next_hour from opa.stream_klines'
            self.curr.execute(query)
            data = self.curr.fetchall()
            print(data)
            return data
        except :
            print("retrieve_stream_price_and_next_hour : unable to do action")
            raise