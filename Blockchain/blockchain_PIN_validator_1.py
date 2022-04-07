#hash is encrypted data of previous_hash,number, data, nonce
#each block consists of 4 data: previous_hash,number,nonce
#.chain takes in all iterables and returns 1 iterable as output

from hashlib import sha256   #library function for encryption 
from itertools import chain
from datetime import datetime

import sys 

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
    global Datetime 
    Datetime = datetime.now()
    #consturctor called to creat an object IN the class Block
    def __init__(self,number=0, previous_hash="0"*64, data=None, nonce=0, datetime=Datetime, PIN = updatehash(Datetime)):   #function1
        self.data = data
        self.number = number
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.datetime = datetime
        self.PIN = PIN
 
    #hash function to pass in number, data and nonce to 'updatehash' as arguments for encryption                            #function3
    #gives envrypted previous_hash, number and previous, data, nonce
    def hash(self):
        return updatehash(
            self.number,
            self.previous_hash,
            self.data,
            self.nonce,
            self.datetime,
            self.PIN)
   
    def __str__(self):                                                                                                      #function2
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
    for i in range (1,max+1):
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
  
        
def main():
    blockchain = BlockChain()
    coins = int(input('Enter number of coins wanted:'))
    
    database = datastore(coins) #database is a list
    
    number = 0
    
    #assign each hash / block 's number
    for data in database: 
       number += 1
       block = Block(number, data=data)
       blockchain.mine(block)  #calling mine function to find previous block's hash
        
    
    empty = ''
    
    for block in blockchain.chain:
        
        empty = empty+str(block)
    #
    #blockchain.chain[2].data = 'New Data'
    #blockchain.mine(blockchain.chain[2])
    #corruption simulation
    
    
    validity = str(blockchain.isValid()) #call 'isValid' function in blockchain class to check validity
    
    return str(f'{validity}!\n{empty}')
    
#prevents executing classes, only running main    


if __name__ == '__main__':  
    coinlog = main()
    print(coinlog)
    filePath = 'coinlog.txt'
    sys.stdout = open(filePath,'w')
    print(str(coinlog))