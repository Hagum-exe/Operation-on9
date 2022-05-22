import mysql.connector
import hashlib
import datetime
import time
mydb = mysql.connector.connect(
    host = "127.0.0.7",
    user = "root",
    password = "Paak93225272"
)
def encrypto(string):
    word = hashlib.sha256(string.encode('utf-8')).hexdigest()
    return word
def deposit():
    amount = input("How much do you want to deposit? ")
    name= input("Enter your name: ")
    cursor = mydb.cursor()
    cursor.execute('UPDATE user SET Crypto_amount = "%s"+Crypto_amount WHERE User_name = "%s"'%(amount,name))
    mydb.commit()
    cursor.close()
def withdraw():
    amount = input("How much do you want to withdraw? ")
    name = input("Enter your name: ")
    cursor = mydb.cursor()
    cursor.execute('UPDATE user SET Crypto_amount = Crypto_amount-"%s" WHERE User_name = "%s"'%(amount,name))
    mydb.commit()
    cursor.close()
    
def register():
    user_name = input("Enter your user name: ")
    gmail = input("Enter your gmail: ")
    password = input("Enter your password: ")
    password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    cursor = mydb.cursor()
    cursor.execute('INSERT INTO user(User_name, Gmail, Password,Crypto_amount) Values("%s","%s","%s",0)'%(user_name,gmail,password))
    mydb.commit()
    cursor.close()
    private_address(user_name,gmail,password)
    
def transact(block):
    nouce =0
    contain = True
    user_from = input("Enter your name: ")
    gmail = input("Enter your gmail: ")
    password= input("Enter your password: ")
    user_to = input("Enter the account's name you want to sent to: ")
    sent_amount = input("Enter the amount: ")
    
    #get user2 data
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM user WHERE User_name = '%s'"%(user_to))
    user2_data = cursor.fetchall()
    for row2 in user2_data:
        pass
    
    #get block data
    cursor = mydb.cursor()
    cursor.execute("SELECT Block_hash FROM block")
    previous = cursor.fetchall()
    print(previous)
    if previous == []:
        print("None")
        contain = False
    else:
        pass
         
    #search for amount
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM user WHERE User_name = '%s'"%(user_from))
    amount = cursor.fetchall()
    for row in amount:
        pass
    if row[4] >0: #if amount is greater than 0
        #get two account's public key
        address,from_date,from_time,nouce1 = public_address(user_from,sent_amount)
        get_address,to_date,to_time,nouce2 = public_address(user_to,sent_amount)
        hash_key,hash_date,hash_time,previous_hash,nouce3 = blockhash(address,get_address,contain,sent_amount)
        verify = verify_hash(hash_key,hash_date,hash_time,user_from,user_to,from_date,from_time,to_date,to_time,sent_amount,contain,nouce1,nouce2,nouce3)#verify the block hash
        if verify == True:
            block += 1
            date = datetime.date.today()
            timing = time.strftime("%H:%M:%S")
            cursor.execute('UPDATE user SET Crypto_amount = "%s"+Crypto_amount WHERE User_name = "%s"'%(sent_amount,user_to))
            cursor.execute('UPDATE user SET Crypto_amount = Crypto_amount - "%s" WHERE User_name = "%s"'%(sent_amount,user_from))
            cursor.execute("INSERT INTO block(User_id,User_id_to,Previous_block_hash,Block_hash,Block,Date,Time) Values('%s','%s','%s','%s','%s','%s','%s')"%(row[0],row2[0],previous_hash,hash_key,block,date,timing))
            

    elif row[4] <=0:
        print("Not enough crypto")
    else:
        print("Error")
    mydb.commit()
    cursor.close()
def change_hash(hash,name):
    cursor = mydb.cursor()
    cursor.execute('UPDATE user SET Public_key = "%s" WHERE User_name = "%s"'%(hash,name))
    mydb.commit()
    cursor.close()
def private_address(name,gmail,password):
    nouce = 0
    while True:
        date = datetime.date.today()
        timing = time.strftime("%H:%M:%S")
        x=name+gmail+password+str(date)+str(timing)+str(nouce)
        private_key = hashlib.sha256(x.encode('utf-8')).hexdigest()
        if private_key[:difficulty] == "0" * difficulty:
            break
        else:
            nouce+=1
    cursor = mydb.cursor()
    cursor.execute("UPDATE user SET Private_key = '%s' WHERE User_name = '%s'"%(private_key,name))
    mydb.commit()
    cursor.close()
def public_address(name,amount):
    nouce=0
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM user WHERE User_name = '%s'"%(name))
    data = cursor.fetchall()
    for column in data:
        pass
    gmail = column[2]
    password = column[3]
    while True:
        date = datetime.date.today()
        timing = time.strftime("%H:%M:%S")
        x = name+gmail+password+str(date)+str(timing)+str(amount)+str(nouce)
        address = hashlib.sha256(x.encode('utf-8')).hexdigest()
        if address[:difficulty] == "0" *difficulty:
            print("X: "+x)
            print("Public address: "+address)
            print("Nouce:"+str(nouce))
            print("DATE: "+str(date))
            print("Time: "+str(timing))
            change_hash(address,name)
            cursor = mydb.cursor()
            cursor.execute("UPDATE user SET Public_key = '%s' WHERE User_name = '%s'"%(address,name))
            return address,date,timing,nouce
        else:
            nouce+=1
            
def blockhash(sent,get,contain,amount):
    nouce = 0
    if contain == True:
        cursor = mydb.cursor()
        cursor.execute("SELECT Block_hash FROM block")
        data = cursor.fetchall()
        for row in data:
            pass
        previous_hash = row[len(row)-1]
        print("Previous: "+previous_hash)
    else:
        previous_hash = "0" * 64
    while True: 
        date = datetime.date.today()
        timing = time.strftime("%H:%M:%S")
        x = str(sent)+str(get)+str(previous_hash)+str(amount)+str(date)+str(timing)+str(nouce)
        hash = hashlib.sha256(str(x).encode('utf-8')).hexdigest()
        if hash[:difficulty] == "0" * difficulty:
            break
        else:
            nouce +=1
    return hash,date,timing,previous_hash,nouce
def drop_table():
    cursor = mydb.cursor()
    cursor.execute("DROP TABLE block")
    mydb.commit()
    cursor.close()
def verify_hash(hash_key,hash_date,hash_time,name,name_to,from_date,from_time,to_date,to_time,amount,contain,nouce1,nouce2,nouce3):
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM user WHERE User_name = '%s'"%(name))
    user1 = cursor.fetchall()
    cursor.execute("SELECT * FROM user WHERE User_name = '%s'"%(name_to))
    user2 = cursor.fetchall()
    for row5 in user1:
        pass
    gmail_from = row5[2]
    pw_from = row5[3]
    for row_to in user2:
        pass
    gmail_to = row_to[2]
    pw_to = row_to[3]
    if contain == True:
        cursor = mydb.cursor()
        cursor.execute("SELECT Block_hash FROM block")
        data = cursor.fetchall()
        for row in data:
            pass
        previous_hash = row[len(row)-1]
        print("previous_hash")
    else:
        previous_hash = "0" * 64

        
    x = name+gmail_from+pw_from+str(from_date)+str(from_time)+str(amount)+str(nouce1)
    public1 = hashlib.sha256(x.encode('utf-8')).hexdigest()

    y = name_to+gmail_to+pw_to+str(to_date)+str(to_time)+str(amount)+str(nouce2)
    address2 = hashlib.sha256(y.encode('utf-8')).hexdigest()
    print("Address2: "+address2)

    print("1: "+public1)
    print("2: "+address2)
    print('3: '+previous_hash)
    print('4:'+str(amount))
    print('5:'+str(hash_date))
    print('6: '+str(hash_time))
    print('7: '+str(nouce3))
    
    z = str(public1)+str(address2)+str(previous_hash)+str(amount)+str(hash_date)+str(hash_time)+str(nouce3)
    verify_hash = hashlib.sha256(z.encode('utf-8')).hexdigest()
    if verify_hash == hash_key:
        print("veryify: ")
        print("Verify_hash: " + verify_hash)
        input()
        return True
    else:
        print("Not verify")
        input()
        print("Verify_hash: " + verify_hash)
        print("hash_key: " + hash_key)
        print("Public1: "+str(public1))
        print("Public2: "+str(address2))
        input()
        return False            
    
def getData():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM user")
    data = cursor.fetchall()
    print(data)

cursor = mydb.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS testCrypto")
cursor.execute("USE testCrypto")
cursor.execute("CREATE TABLE IF NOT EXISTS user(User_id int auto_increment primary key,User_name varchar(20),Gmail varchar(30),Password varchar(100),Crypto_amount decimal(10,2),Public_key varchar(100),Private_key varchar(100),Hash_key varchar(100))")
cursor.execute("CREATE TABLE IF NOT EXISTS block(User_id int ,User_id_to int,Previous_block_hash varchar(100),Block_hash varchar(100) primary key,Block int,Time varchar(8),Date varchar(10),Valid varchar(5))")
mydb.commit()
cursor.close()
difficulty = 4
block = 0
name = "joshua"
gmail = "joshuakwongty@gmail.com"
password = "joshuapw12345"




transact(block)









