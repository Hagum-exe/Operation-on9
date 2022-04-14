#from app_test import database
import mysql.connector
from tkinter import END  

from mysql_connect import SQLdb


class Table():
    
    def __init__(self, table_name, *args):
        self.table = table_name
        self.columns = "(%s)" %",".join(args)
        self.columnsList = args


    def insert(self, *data):
        from mysql_connect import SQLdb
        print(str(data))
        create_data =""
        for datum in data:
            create_data += f"'{datum}',"
    #dataNames = dataNames[:len(dataNames)-1]
        cursor = SQLdb.cursor()
        cursor.execute("INSERT INTO %s%s VALUES(%s)" %(self.table, self.columns,create_data[:len(create_data)-1]))
        SQLdb.commit()
   

   
  





