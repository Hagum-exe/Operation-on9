import mysql.connector

mydb = mysql.connector.connect(
    user = 'root',
    password = 'dwjk7158',
    host = 'localhost',
    database = 'crypto')




cursor = mydb.cursor()
cursor.execute("USE crypto")
cursor.execute("SELECT * FROM users")
data = cursor.fetchall()
for row in data:
    print("Name: "+row[0]+";")
    print("gmail: "+row[1]+";")
    print("User name "+row[2]+";")
    print("Password: "+row[3]+";")
    print("Coin mine: "+row[4]+";")
    print("Balance: "+str(row[5])+";","\n")
