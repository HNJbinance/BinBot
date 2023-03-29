import logging
from termcolor import colored
import modules.sql_properties as sql 
# from binance.lib.utils import config_logging
from binance  import ThreadedWebsocketManager
import json

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


sql = sql.SqlAction()
def main():


    twm = ThreadedWebsocketManager()
    # start is required to initialise its internal loop
    twm.start()

    def handle_socket_message(msg):
        # storing usefull data into new dict
        new_message = msg['k']

        # adding event_time to new_dict
        new_message['event_time'] = msg['E']

        #storting data into database
        sql.store_stream_klines(new_message)



    symint = sql.get_symbol_interval()
    # loop on every symbol/interval requested
    for val in symint :        
        db_interval=val['interval_symbol']
        db_symbol = val['symbol'].lower()
        twm.start_kline_socket(callback=handle_socket_message, symbol=db_symbol, interval=db_interval)

        # multiple sockets can be started
    twm.join()


if __name__ == '__main__':
   main()
