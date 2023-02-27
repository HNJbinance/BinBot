from binance.spot import Spot
import modules.sql_properties as sql 
import pprint as pprint
from termcolor import colored
from time import sleep

# info maximum limit request API : 1,200 request weight per minute
# if rule break : http 403 with ban period of 5 min

client = Spot()
sql = sql.SqlAction()

# print(client.time())
db_next_startime = 0
starttime = 1
i=0
max_loop =1000
while ( db_next_startime < starttime and i < max_loop ) : 
    
    # get symbol interval data to retrieve historical data from database
    symint = sql.get_symbol_interval()
    # loop on every symbol/interval requested
    for val in symint :
        # db variables   
        db_id_symint = val['id_symint']
        db_next_startime = val['endtime']+1
        db_interval=val['interval_symbol']
        db_symbol = val['symbol']
        
        # get historical data of symbol/interval requested from binance REST API
        klines_data =  client.klines(symbol=db_symbol, interval=db_interval,startTime=db_next_startime)
        # Remove last index of each list (// Unused field. Ignore.)
        klines_data = [klines_data[:-1] for klines_data in klines_data]

        # api variables  
        lenght_list = len(klines_data)-1    
        starttime = klines_data[0][0] if lenght_list>0 else 0
        endtime = klines_data[lenght_list][0] if lenght_list>0 else 0
       
        print(colored('get_historical_date : db_id_symint:{}, db_symbol:{}, db_interval:{}, db_starttime:{}, db_endtime:{}'.format(db_id_symint, val['symbol'], val['interval_symbol'], val['starttime'], val['endtime']),"green"))
        print(colored('get_historical_date : api_next_starttime:{}, api_next_endtime:{}'.format(starttime,endtime),"yellow"))

        if lenght_list > 0 :
            # Storing API result into database
            sql.store_historical_klines(db_id_symint,klines_data)

            # Update last stoptime into database
            sql.update_symbol_interval(db_id_symint,endtime)

            # Waiting for API limitation
            sleep(1)
            i += 1
else :
    if db_next_startime > starttime : 
         print(colored("get_historical_date : historical data is up to date" ,'green'))
    elif i > max_loop :
        print(colored("get_historical_date : max_loop is reached please launch again" ,'green'))




         
 


