def main():

    from binance.spot import Spot
    import modules.sql_properties as sql  

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

    # info maximum limit request API : 1,200 request weight per minute
    # if rule break : http 403 with ban period of 5 min

    client = Spot(timeout=2)
    sql = sql.SqlAction()
    max_open_time = sql.retrieve_last_open_time()[0]['open_time']
    if max_open_time is None or max_open_time==0 :
        max_open_time = 1
    print(max_open_time)
    # variables   
    api_starttime = 0
    api_endtime = 1
    i = 0
    max_loop = 100000 

    db_symbol = 'BTCUSDT'
    db_interval = '1h'

    api_endtime = max_open_time
    print('get_historical_date : db_symbol:{}, db_interval:{}'.format(db_symbol,db_interval))

    while (api_starttime < api_endtime and i < max_loop ) : 
        # get historical data of symbol/interval requested from binance REST API
        klines_data =  client.klines(symbol=db_symbol, interval=db_interval,startTime=api_endtime-1,limit=1000)
        # Remove last index of each list (// Unused field. Ignore.)
        klines_data = [klines_data[:-1] for klines_data in klines_data]

        # api variables  
        lenght_list = len(klines_data)-1    
        api_starttime = klines_data[0][0] if lenght_list>0 else 0
        api_endtime = klines_data[lenght_list][0] if lenght_list>0 else 0

        print('get_historical_date : api_starttime:{}, api_endtime:{}'.format(api_starttime,api_endtime))
  
        if lenght_list >= 0 :
            # Storing API result into database
            print(klines_data)
            sql.store_historical_klines(db_symbol,db_interval,klines_data)

            i += 1
    else :        
        if max_open_time > api_starttime : 
            print("get_historical_date : historical data is up to date" )
        elif i > max_loop :
            print("get_historical_date : max_loop is reached please launch again" )  


if __name__ == '__main__':
   main()




            
    


