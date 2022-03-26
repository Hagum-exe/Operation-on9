#hash is encrypted data of previous_hash,number, data, nonce
#each block consists of 4 data: previous_hash,number,nonce
#.chain takes in all iterables and returns 1 iterable as output

from hashlib import sha256  #library function for encryption 


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
    

    #consturctor called to creat an object IN the class Block
    def __init__(self,number=0, previous_hash="0"*64, data=None, nonce=0):
        self.data = data
        self.number = number
        self.previous_hash = previous_hash
        self.nonce = nonce

 
    #hash function to pass in number, data and nonce to 'updatehash' as arguments for encryption
    #gives envrypted previous_hash, number and previous, data, nonce
    def hash(self):
        return updatehash(self.previous_hash, self.number, self.data, self.nonce)
    
    def __str__(self):   #does NOT give the number of hash / block
        return str(f'Block#: {self.number}\n Hash: {self.hash()}\n Previous hash: {self.previous_hash}\n Data: {self.data}\n Nonce: {self.nonce}%\n ' )   
                                                         #gives encrypted hash text with Hash:
class BlockChain():
    global difficulty
    difficulty = 4  #produces 4 0s at the front of the hash
    
    
    def __init__(self, chain=[]):
        self.chain = chain        #add chain to constructor if chain exists
        
    def add(self, block):    #define what adding a block to a chain looks like
        self.chain.append({'hash': block.hash(), 'previous_hash': block.previous_hash, 'number': block.number, 'data': block.data})
                                          #put each single block data into chain 
    def mine(self, block):
       try:
           block.previous_hash = self.chain[-1].get('hash')  #get the last Hash of the last chain
        
       except IndexError:
           pass    #pass if there is no previous hash / block
        
       while True:   #while no break statement
            if block.hash()[:4] == '0' * difficulty:  #if the first 4 chars in the hash is 4*0s
               self.add(block) 
               break
                
            else:  #else add 1 to nonce
                block.nonce +=1
  
            
        
        
        
        

def main():
    blockchain = BlockChain()
    database = ['on9_1', 'on9_2', 'on9_3', 'on9_4']
    
    num = 0
    
    #assign each hash / block 's number
    for data in database: 
        num += 1
        blockchain.mine(Block(data, num))    #calling mine function to find previous block's hash
        

    for block in blockchain.chain:
        print(block)  #print information of each block in the blockchain
        
    

   
#prevents executing classes, only running main    
if __name__ == '__main__':  
    main()
    
