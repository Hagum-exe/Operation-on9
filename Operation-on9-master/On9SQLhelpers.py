#function file for 'On9app'
#mainly SQL functions 
import mysql.connector
from tkinter import END  
from loginSQL import SQLdb
from On9blockchain import Block, Blockchain
class InvalidTransactionException():
    pass

class InsufficientFundsException():
    pass

class Table():         #Table class to get 'table_name' and 'columns' for more convenient function building
  
    def __init__(self, table_name, *args):
        self.table = table_name
        self.columns = "(%s)" %",".join(args)
        self.columnsList = args
        
    def updateData(self,setColumn, newValue,  searchColumn ,searchValue):
        cursor = SQLdb.cursor()
        cursor.execute('UPDATE %s SET %s="%s" WHERE %s="%s"' %(self.table, setColumn, newValue, searchColumn, searchValue))
        SQLdb.commit()
        cursor.close()    
    
    def insert(self, *data):          #insert function for adding data to table
        
        create_data =""
        for datum in data:
            create_data += f"'{datum}',"
        cursor = SQLdb.cursor()
        cursor.execute("INSERT INTO %s%s VALUES(%s)" %(self.table, self.columns,create_data[:len(create_data)-1]))
        SQLdb.commit()
        cursor.close()
    
    def selectAll(self):          #select all from the table and returns all data
        cursor = SQLdb.cursor()
        result = cursor.execute("SELECT * FROM %s" %self.table)
        data = cursor.fetchall()
        return data

    def selectColumn(self, columnName):   #select specific column from table
        cursor = SQLdb.cursor()
        cursor.execute("SELECT %s FROM %s" % (columnName, self.table))
        result = cursor.fetchall()
        cursor.close()
        return result
    
    
    def selectRow(self, columnName, value):   #select a row from table, can belong to users or blocks
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
                                                               #select a specific data from the table
                                                               #'SELECT wanted_column FROM table where column = conditional value
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
        
     
    
    
    def deleteOneRow(self, columnName, value):    #delete a single row from the table
        
        cursor = SQLdb.cursor()
        cursor.execute('DELETE from %s where %s = "%s"' %(self.table, columnName, value))
        SQLdb.commit()
        cursor.close()
        
    def deleteAllFromTable(self):   #delete all data from table but keeps table
        cursor = SQLdb.cursor()
        cursor.execute("DELETE FROM %s" % self.table)
        SQLdb.commit()
        cursor.close()
     
    def drop(self):               #delete the whole table including all data
        cursor = SQLdb.cursor()
        cursor.execute("DROP TABLE %s" %self.table)
        cursor.close()

#end of class Table 
 
        
def isnewuser(username):           #check if username is a new user
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
    

def lastBlockNum():    #gets the last block number from the 'blockchain' table
    blockchain = Table('blockchain', 'number', 'hash', 'previous', 'data', 'nonce', 'datetime')
    
    blockNumbers = blockchain.selectColumn('number')

    if not blockNumbers:
        return 0
    else:
        blockNumber = int(str(blockNumbers[-1])[2])
        return blockNumber



def selectBlock(blockName):   #gets a block according to its name
    blockchain = Table('blockchain', 'number', 'hash', 'previous', 'data', 'nonce', 'datetime')
    
    block = blockchain.selectRow('data',blockName)
    return block

def selectBlockchain():
    
    blockchain = Table('blockchain', 'number', 'hash', 'previous', 'data', 'nonce', 'datetime')
    allBlockchain = blockchain.selectAll()
    return allBlockchain


def deleteBlockchain (*blockNames):  #delete a specific block from the Table
    blockchain = Table('blockchain', 'number', 'hash', 'previous', 'data', 'nonce', 'datetime')
    
    for blockName in blockNames:
        blockchain.deleteOneRow('data',blockName)



     
def getBlockchain():
    blockchain = Blockchain()
    blockchainSQL = Table('blockchain', 'number', 'hash', 'previous', 'data', 'nonce', 'datetime')
    for block in blockchainSQL.selectAll():
        
        blockchain.add(Block(int(block[0]), block[2], block[3], int(block[4]), block[5]))
    return blockchain

def getBalance(username):
    balance = 0.00
    blockchain = getBlockchain()

    #loop through the blockchain and update balance
    for block in blockchain.chain:
        data = block.data.split("-->")
        if username == data[0]:
            balance -= float(data[2])
        elif username == data[1]:
            balance += float(data[2])
    return balance

def syncBlockChain(blockchain):
    blockchainSQL = Table('blockchain', 'number', 'hash', 'previous', 'data', 'nonce', 'datetime')     
    blockchainSQL.deleteAllFromTable()
    
    for block in blockchain.chain:
        blockchainSQL.insert(str(block.number), block.hash(), block.previous_hash, block.data, block.nonce, block.datetime)

def sendMoney(sender, recipient, amount): 
    try:
        amount = float(amount)
    except ValueError:
        raise InvalidTransactionException('Invalid Transaction data type.')
    
    if amount > getBalance(sender) and sender != 'On9admin':
        raise InsufficientFundsException('Insufficient funds.')
    
    if sender == recipient or amount <=0.00:
        raise InvalidTransactionException('Invalid Transaction')
  
    elif isnewuser(recipient):
        raise InvalidTransactionException('Sender Does Not exist')
    blockchain = getBlockchain()
    number = lastBlockNum()+1
    data = "%s-->%s-->%s" %(sender, recipient, str(amount))
    block = Block(number, data=data)
    blockchain.mine(block)
    syncBlockChain(blockchain)

print(getBalance('testman'))