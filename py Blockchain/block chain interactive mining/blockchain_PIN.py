#hash is encrypted data of previous_hash,number, data, nonce
#each block consists of 4 data: previous_hash,number,nonce
#.chain takes in all iterables and returns 1 iterable as output

from hashlib import sha256
from itertools import chain
from sqlite3 import Date
from time import time  #library function for encryption 
from datetime import datetime
from turtle import update
import sys 

#updatehash function
#return encrypted data
def updatehash(*args):
    hashingText = ''
    h = sha256()
    for arg in args:
        hashingText += str(arg)  #adding each arguments to hashingText
        
    h.update(hashingText.encode('utf8')) #using 'utf8' in sha256 to encrypt arguments 
    return h.hexdigest()                 #returns the encrypted text as hex strings

    
#Block function creating block
#returns str(hash, previous_hash, data, nonce)
class Block():
    global Datetime 
    Datetime = datetime.now()
    #consturctor called to creat an object IN the class Block
    def __init__(self,number=0, previous_hash="0"*64, data=None, nonce=0, datetime=Datetime, PIN = updatehash(Datetime)):
        self.data = data
        self.number = number
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.datetime = datetime
        self.PIN = PIN
 
    #hash function to pass in number, data and nonce to 'updatehash' as arguments for encryption
    #gives envrypted previous_hash, number and previous, data, nonce
    def hash(self):
        return updatehash(
            self.number,
            self.previous_hash,
            self.data,
            self.nonce,
            self.datetime,
            self.PIN)
   
    def __str__(self):
        return str("Block#: %s;\nHash: %s;\nPrevious: %s;\nData: %s;\nNonce: %s;\nDatetime: %s;\nPIN: %s;\n!\n" %(
            self.number,
            self.hash(),
            self.previous_hash,
            self.data,
            self.nonce,
            str(self.datetime),
            str(self.PIN)
            )
        )
                                                         #gives encrypted hash text with Hash:
class BlockChain():
    
    difficulty = 4  #produces 4 0s at the front of the hash
    
    
    def __init__(self):
        self.chain = []
   #add chain to constructor if chain exists
        
    def add(self, block):    #define what adding a block to a chain looks like
        self.chain.append(block) #put each single block data into chain 
    def mine(self, block):
       
       try: block.previous_hash = self.chain[-1].hash()  #get the last Hash of the last chain
        
       except IndexError: pass
             #pass if there is no previous hash / block
        
       while True:
            if block.hash()[:self.difficulty] == "0" * self.difficulty:
                self.add(block); break
                
            else:  #else add 1 to nonce
                block.nonce +=1
  
def datastore(max):
   
    DatabaseStr = ''
    for i in range (1,max+1):
        data = '-on9_'+str(i)
        DatabaseStr = DatabaseStr + data
    
    Database =  list(DatabaseStr.split('-')) 
    
    Database.remove('')
    empty = ''
    for i in Database:
        empty = empty + i + ' '
        
    print(empty)
          
    
    return Database
  
        
def main():
    blockchain = BlockChain()
    coins = int(input('Enter number of coins wanted:'))
    
    database = datastore(coins)
    
    num = 0
    
    #assign each hash / block 's number
    for data in database: 
       num += 1
       blockchain.mine(Block(num, data=data))#calling mine function to find previous block's hash
        
    
    empty = ''
    
    for block in blockchain.chain:
        #print(block)  #print information of each block in the blockchain
        empty = empty+str(block)
        
    print(empty)
    return empty
    
#prevents executing classes, only running main    


if __name__ == '__main__':  
    coinlog = main()
    print(coinlog)
    filePath = 'coinlog.txt'
    sys.stdout = open(filePath,'w')
    print(str(coinlog))