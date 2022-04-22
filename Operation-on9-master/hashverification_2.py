from time import time
from tkinter import END  




def logcompare(org, blockchainData):   #compares the input PIN and the real PIN
    global coinPIN
    
    
    for i in range (1,len(blockchainData)-1):
      
        block = blockchainData[i]
        dataOfBlock = list(block.split(';'))  
        blockNumber = i
        #print(blockNumber)
        blockHash = dataOfBlock[1][7:]
        #print(blockHash)
        blockPIN = dataOfBlock[6][6:]
        #print(blockPIN)
        i += 1
        if org == blockHash:
            coinPIN = blockPIN
            return True
            
    return False       
        
def examineBlockChain(org, coinlog):
    coinData_valid =  list(coinlog.split('!')) 
   
    validity = str(list(coinlog.split('!'))[0])
    if validity != 'True':
        print('Blockchain is NOT valid')
        return False
    else:
        print('Blockchain is valid')
        return coinData_valid
  
    
def PinVerification(PINInput, coinPIN):
    if PINInput == coinPIN:
        return True
    
    else:
        return False
    
    
    


#main


with open('coinlog.txt') as f:
    coinlog = f.read()
    #print(coinlog)
    

#print(f'the blockchain is: {validity} lol')
    
realHash = str(input('Enter Hash of the coin: '))

examineValid = examineBlockChain(realHash, coinlog)

if examineValid == False:
    END

else:
      
    exist = logcompare(realHash, examineValid)

    print(f'Coin exist? {exist}')


    if exist == True:
        PINinput = str(input('Enter PIN:'))
        examinePIN = PinVerification(PINinput, coinPIN)
        print(f'The PIN is correct? {examinePIN}')
    
        if examinePIN == True:
            print('coin verified')
        
        else:
            print('coin not verified')




    
    

