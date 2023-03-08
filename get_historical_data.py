
#!/usr/bin/python
from binance.spot import Spot
import modules.sql_properties as sql 
import pprint as pprint
from termcolor import colored
from time import sleep

from os import getpid
from sys import argv, exit
import psutil  ## pip install psutil

myname = argv[0]
mypid = getpid()
print(myname)
for process in psutil.process_iter():
    if process.pid != mypid:
        for path in process.cmdline():
            if myname in path:
                print("process found")
                process.terminate()
                sleep(0.5)

# info maximum limit request API : 1,200 request weight per minute
# if rule break : http 403 with ban period of 5 min

client = Spot(timeout=2)
sql = sql.SqlAction()
max_speed = 60/300
# print(client.time())

# get symbol interval data to retrieve historical data from database
symint = sql.get_symbol_interval()
# loop on every symbol/interval requested
for val in symint :    
    # variables   
    api_starttime = 0
    api_endtime =1
    i = 0
    max_loop =10000 
    # db variables   
    db_id_symint = val['id_symint']
    db_starttime = val['starttime']
    db_endtime = val['endtime']
    db_interval=val['interval_symbol']
    db_symbol = val['symbol']
    
    api_starttime == db_endtime
    print(colored('get_historical_date : db_id_symint:{}, db_symbol:{}, db_interval:{}, db_starttime:{}, db_endtime:{}'.format(db_id_symint, val['symbol'], val['interval_symbol'], val['starttime'], val['endtime']),"green"))

    while ( api_starttime < api_endtime and i < max_loop ) : 
        # get historical data of symbol/interval requested from binance REST API
        klines_data =  client.klines(symbol=db_symbol, interval=db_interval,startTime=db_endtime+1,limit=1000)
        # Remove last index of each list (// Unused field. Ignore.)
        klines_data = [klines_data[:-1] for klines_data in klines_data]

        # api variables  
        lenght_list = len(klines_data)-1    
        api_starttime = klines_data[0][0] if lenght_list>0 else 0
        api_endtime = klines_data[lenght_list][0] if lenght_list>0 else 0
    
        print(colored('get_historical_date : api_starttime:{}, api_endtime:{}'.format(api_starttime,api_endtime),"yellow"))

        if lenght_list > 0 :
            # Storing API result into database
            sql.store_historical_klines(db_id_symint,klines_data)

            # Update last stoptime into database
            sql.update_symbol_interval_endtime(db_id_symint,api_endtime)
            db_endtime = api_endtime

            if db_starttime == 0 : 
                # Update first starttime into database
                sql.update_symbol_interval_starttime(db_id_symint,api_starttime)
                db_starttime = api_starttime

            # Waiting for API limitation
            sleep(max_speed)
            i += 1
    else :
        if db_endtime > api_starttime : 
            print(colored("get_historical_date : historical data is up to date" ,'green'))
        elif i > max_loop :
            print(colored("get_historical_date : max_loop is reached please launch again" ,'green'))




         
 


