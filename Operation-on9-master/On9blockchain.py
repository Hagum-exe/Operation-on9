from hashlib import sha256
from datetime import datetime
#Takes in any number of arguments and produces a sha256 hash as a result
def updatehash(*args):
    hashing_text = ""; h = sha256()

    #loop through each argument and hash
    for arg in args:
        hashing_text += str(arg)

    h.update(hashing_text.encode('utf-8'))
    return h.hexdigest()

#The "node" of the blockchain. Points to the previous block by its unique hash in previous_hash.
class Block():

    #default data for block defined in constructor. Minimum specified should be number and data.
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
        


#The "LinkedList" of the blocks-- a chain of blocks.
class Blockchain():
    #the number of zeros in front of each hash
    difficulty = 4

    #restarts a new blockchain or the existing one upon initialization
    def __init__(self):
        self.chain = []

    #add a new block to the chain
    def add(self, block):
        self.chain.append(block)

    #remove a block from the chain
    def remove(self, block):
        self.chain.remove(block)

    #find the nonce of the block that satisfies the difficulty and add to chain
    def mine(self, block):
        #attempt to get the hash of the previous block.
        #this should raise an IndexError if this is the first block.
        try: block.previous_hash = self.chain[-1].hash()
        except IndexError: pass

        #loop until nonce that satisifeis difficulty is found
        while True:
            if block.hash()[:self.difficulty] == "0" * self.difficulty:
                self.add(block); break
            else:
                #increase the nonce by one and try again
                block.nonce += 1

    #check if blockchain is valid
    def isValid(self):
        #loop through blockchain
        for i in range(1,len(self.chain)):
            _previous = self.chain[i].previous_hash
            _current = self.chain[i-1].hash()
            #compare the previous hash to the actual hash of the previous block
            if _previous != _current or _current[:self.difficulty] != "0"*self.difficulty:
                return False

        return True

