#hash is encrypted data of previous_hash,number, data, nonce
#each block consists of 4 data: previous_hash,number,nonce
#.chain takes in all iterables and returns 1 iterable as output
import time
from hashlib import sha256   #library function for encryption 
from itertools import chain
from datetime import datetime

from On9SQLhelpers import *


#read from MySQL database 'crypto' table 'blockchain'



#updatehash function
#return encrypted data
def updatehash(*args):     #exchange args to 64 bit letters
    hashingText = ''
    h = sha256()
    for arg in args:
        hashingText += str(arg)  #adding each arguments to hashingText
        
    h.update(hashingText.encode('utf8')) #using 'utf8' in sha256 to encrypt arguments 
    return h.hexdigest()                 #returns the encrypted text as hex strings

    
#Block function creating block
#returns str(hash, previous_hash, data, nonce)
class Block():
    #global Datetime 
 
    Datetime = datetime.now()
    
    #consturctor called to creat an object IN the class Block
    
    def __init__(self,number=0, previous_hash="0"*64, data=None, nonce=0, datetime=Datetime):   #function1
        self.data = data
        self.number = number
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.datetime = datetime
        
 
    #hash function to pass in number, data and nonce to 'updatehash' as arguments for encryption                            #function3
    #gives envrypted previous_hash, number and previous, data, nonce
    def hash(self):
        return updatehash(
            self.number,
            self.previous_hash,
            self.data,
            self.nonce,
            self.datetime,)
   
    def PINhash(self):
       return updatehash(self.nonce, self.datetime)
       
       
           
    def __str__(self):                                                                                                    #function2
        blockchain = Table('blockchain', 'number', 'hash', 'previous', 'data', 'nonce', 'datetime', 'PIN', 'transData')
        blockchain.insert(self.number, self.hash(), self.previous_hash, self.data, self.nonce, str(self.datetime), self.PINhash(), 'admin_user')
        #insert blockchain data into table 'blockchain' 
       
        
        global blockNumber
        blockNumber = self.number
        
        return str("Block#: %s;\nHash: %s;\nPrevious: %s;\nData: %s;\nNonce: %s;\nDatetime: %s;\nPIN: %s;\n!\n" %(
            self.number,
            self.hash(),
            self.previous_hash,
            self.data,
            self.nonce,
            str(self.datetime),
            self.PINhash()
            )
        )
                                                         #gives encrypted hash text with Hash:
class BlockChain():
    
    difficulty = 4  #produces 4 0s at the front of the hash
    
    
    def __init__(self):
        self.chain = []   #it is a list         [''hi', 'i am'', ''hallee', 'joshua'']
   #add chain to constructor if chain exists
        
    def add(self, block):    #define what adding a block to a chain looks like
        self.chain.append(block) #put each single block data into chain 
    def mine(self, block):
       
       try: block.previous_hash = self.chain[-1].hash()  #get the last Hash of the last chain
        
       except IndexError: pass
             #pass if there is no previous hash / blockY
        
       while True:
            if block.hash()[:self.difficulty] == "0" * self.difficulty: #try to make the hash start with four zero
                self.add(block); break
                
            else:  #else add 1 to nonce                                  if can't nonce += 1
                block.nonce +=1
                
    def isValid(self):
        #loop through blockchain
        for i in range(1,len(self.chain)):
            _previous = self.chain[i].previous_hash
            _current = self.chain[i-1].hash()
            #compare the previous hash to the actual hash of the previous block
            if _previous != _current or _current[:self.difficulty] != "0"*self.difficulty:
                return False

        return True
                
  
def datastore(max):
   
    DatabaseStr = ''
    for i in range (minBlockNum,minBlockNum+max):
        data = '-on9_'+str(i)       #-on9_1    #-on9_2   #-on9_3

        DatabaseStr = DatabaseStr + data
      # databaseStr = -on9_1-on9_2-on9_3
    Database =  list(DatabaseStr.split('-')) 
    Database.remove('')
    empty = ''
    for data in Database:
        empty = empty + data + ' '
        
    print(empty)
          
    
    return Database   #return variable to global
  
        
def main(amount):
    global minBlockNum
    minBlockNum = lastBlockNum() + 1
    number = minBlockNum-1
    
    blockchain = BlockChain()
    coins = amount
    
    database = datastore(coins) #database is a list
    
    
    
    #assign each hash / block 's number
    for data in database: 
       number += 1
       block = Block(number, data=data)
       blockchain.mine(block)  #calling mine function to find previous block's hash
 
    
    numberStore = ""
    
    for block in blockchain.chain:
        
        print(block)
        numberStore += str(blockNumber)
        #print('Num:', blockNumber)
        #empty = empty+str(block)
   
    
    validity = str(blockchain.isValid()) #call 'isValid' function in blockchain class to check validity
    print(validity)
    
    chaincheck = Table('chaincheck', 'number', 'isvalid')
    for number in numberStore:
        chaincheck.insert(number, str(validity))     #insert number of blocks and its corresponding validity
        
    
    #return str(f'{validity}!\n{empty}')
    
#prevents executing classes, only running main    


if __name__ == '__main__':  
    coinwanted = int(input('Enter number of coins wanted:'))
    main(coinwanted)