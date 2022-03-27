import hashlib


from hashlib import sha256
from this import d
from time import time  #library function for encryption 


def updatehash(*args):
    hashingText = ''
    h = sha256()
    for arg in args:
        hashingText += str(arg)  #adding each arguments to hashingText
        
    h.update(hashingText.encode('utf8')) #using 'utf8' in sha256 to encrypt arguments 
    return h.hexdigest()                 #returns the encrypted text as hex strings

def compare(orgHash, newHash):
    if orgHash == newHash:
        return True
    
    else:
        return False

number = str(input('enter number of coin:'))
hash = str(input('Enter hash:'))
previous_hash = str(input('Previous hash:'))
data = str(input('Enter name of hash:')) 
nonce = str(input('Nonce:'))
datetime = str(input('Enter datetime:'))

newhash = updatehash(number,  previous_hash, data, nonce, datetime)


print(f'org hash is:{hash}')
print(f'new hash is:{newhash}')
print(f'the hash is valid? : {compare(hash, newhash)}')


#Block#: 5
#Hash: 00006a266d59f492ec63ffb5112bafb0b9bb4ae2fb9d3259b4c2d7f325469057
#Previous: 00009e8f600d13b51fdf79c07d35956a7fa1d3869aff8495bcef8beedc3f93b6
#Data: on9_5
#Nonce: 23644
#Datetime: 2022-03-27 22:17:50.907784