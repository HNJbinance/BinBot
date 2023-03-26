import modules.sql_properties as sql 
from time import sleep
from termcolor import colored 

sql = sql.SqlAction()


id_symint = 1 
list = sql.retrieve_historical_klines(id_symint)




print(colored("\ndb data info :","green"))
print(type(list))
print(colored("\nnb lines : ","green"))
print(len(list))
print(colored("\nexemple : ","green"))
print(list[0])





