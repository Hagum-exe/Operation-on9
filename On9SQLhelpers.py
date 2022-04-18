#from app_test import database
import mysql.connector
from tkinter import END  
from loginSQL import SQLdb


class Table():
  
    def __init__(self, table_name, *args):
        self.table = table_name
        self.columns = "(%s)" %",".join(args)
        self.columnsList = args
        
        
    def insert(self, *data):
        #from mysql_connect import SQLdb
        #print(str(data))
        create_data =""
        for datum in data:
            create_data += f"'{datum}',"
        cursor = SQLdb.cursor()
        cursor.execute("INSERT INTO %s%s VALUES(%s)" %(self.table, self.columns,create_data[:len(create_data)-1]))
        SQLdb.commit()
        cursor.close()
    
    def selectAll(self):
        cursor = SQLdb.cursor()
        result = cursor.execute("SELECT * FROM %s" %self.table)
        data = cursor.fetchall()
        return data

    def selectColumn(self, columnName):
        cursor = SQLdb.cursor()
        cursor.execute("SELECT %s FROM %s" % (columnName, self.table))
        result = cursor.fetchall()
        cursor.close()
        return result
    
    
    def selectRow(self, columnName, value):
        data = {}
        cursor = SQLdb.cursor()
        results = cursor.execute('SELECT * FROM %s WHERE %s = "%s"' %(self.table, columnName, value))
        data = cursor.fetchall()
        #if results != None and results.count() > 0:
        #    data = cursor.fetchone()
            
        #else:
        #    data = cursor.fetchall()    
            
        cursor.close()
        return data
    
    def selectOneData(self,  searchColumn,columnName, value):  #searchColumn = wanted value's column
        data = {}
        cursor = SQLdb.cursor()
        results = cursor.execute('SELECT %s FROM %s WHERE %s = "%s"' %(searchColumn, self.table, columnName, value))
        data = cursor.fetchall()
        cursor.close()
        if len(data) == 0:
            return None
        
        else:
            realData = "".join(data[0])
            return realData
        
     
    
    
    def deleteOneRow(self, columnName, value):
        
        cursor = SQLdb.cursor()
        cursor.execute('DELETE from %s where %s = "%s"' %(self.table, columnName, value))
        SQLdb.commit()
        cursor.close()
        
    def deleteAllFromTable(self):
        cursor = SQLdb.cursor()
        cursor.execute("DELETE FROM %s" % self.table)
        SQLdb.commit()
        cursor.close()
    
    def drop(self):
        cursor = SQLdb.cursor()
        cursor.execute("DROP TABLE %s" %self.table)
        cursor.close()
        
def isnewuser(username):
    #access the users table and get all values from column "username"
    users = Table("users", "name", "email", "username", "password")
    usernamesList = (users.selectColumn('username'))
    
    realUserName = tuple(map(str, username.split()))
    
    if usernamesList == []:
        return False
    elif realUserName in usernamesList : 
        return False 
    else: 
        return True
    
def lastBlockNum():
    blockchain = Table('blockchain', 'number', 'hash', 'previous', 'data', 'nonce', 'datetime', 'PIN')
    
    blockNumbers = blockchain.selectColumn('number')

    if not blockNumbers:
        return 0
    else:
        blockNumber = int(str(blockNumbers[-1])[2])
        return blockNumber



def selectBlock(blockName):
    blockchain = Table('blockchain', 'number', 'hash', 'previous', 'data', 'nonce', 'datetime', 'PIN')
    
    block = blockchain.selectRow('data',blockName)
    return block

def deleteBlockchain (*blockNames):
    blockchain = Table('blockchain', 'number', 'hash', 'previous', 'data', 'nonce', 'datetime', 'PIN')
    
    for blockName in blockNames:
        blockchain.deleteOneRow('data',blockName)

