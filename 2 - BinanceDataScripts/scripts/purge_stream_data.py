
import modules.sql_properties as sql 
from os import getpid
from sys import argv
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
# Purge stream_klines_tables
sql.purge_stream_klines()
