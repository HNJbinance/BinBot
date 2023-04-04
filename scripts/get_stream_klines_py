def main():

    from binance.websocket.spot.websocket_client import SpotWebsocketClient
    import modules.sql_properties as sql 

    sql = sql.SqlAction()
    #####################################
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
    #####################################

    ws_client  = SpotWebsocketClient()
    ws_client.start()
    def handle_socket_message(msg):        
        # #store data into database
        try : 
            if 'k' in msg.keys() :
                # # storing usefull data into new dict           
                new_message = msg['k']
                new_message['event_time'] = msg['E']
                # storting data into database                
                sql.store_stream_klines(new_message)
                # print(msg)
            else :
                pass
        except Exception:
            ws_client.stop()
            raise          

    # retrieve symbol/interval requested
    db_symbol = 'BTCUSDT'
    db_interval = '1h'
    ws_client .kline(callback=handle_socket_message, id=1, symbol=db_symbol, interval=db_interval)
    ws_client.join()


if __name__ == '__main__':
   main()


