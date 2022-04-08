import hashlib


from hashlib import sha256
from this import d
from time import time  #library function for encryption 

import sys




def logcompare(org, coinlog):
    coinData =  list(coinlog.split('!')) 
    global coinPIN
    
    
    for i  in range (len(coinData)-1):
        coin = coinData[i]
        
        if i == 0:
            blocknum = list(coin.split(';'))[0][9::]
        else:
            blocknum = list(coin.split(';'))[0][10::]
        blockPIN = list(coin.split(';'))[5][6::]
        Hash = list(coin.split(';'))[1][7::]
        #print(f'{blocknum}\n{Hash}\n{blockPIN}\n')
    
        if org == Hash:
            coinPIN = blockPIN
            return True
            
    return False       
        
    
def PinVerification(PINInput, coinPIN):
    if PINInput == coinPIN:
        return True
    
    else:
        return False
    
    
    


#main


with open('coinlog.txt') as f:
    coinlog = f.read()
    #print(coinlog)

realHash = str(input('Enter Hash of the coin: '))
exist = logcompare(realHash, coinlog)
print(f'Coin exist? {exist}')

    
if exist == True:
    PINinput = str(input('Enter PIN:'))
    corrPIN = PinVerification(PINinput, coinPIN)
    print(f'The PIN is correct? {corrPIN}')
    
    if corrPIN == True:
        print('coin verified')
        
    else:
        print('coin not verified')




    
    

