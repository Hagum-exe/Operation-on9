from flask_mysqldb import MySQLdb
import mysql.connector


database = mysql.connector.connect(          # using 'mysql.connector'
    host = 'localhost',  #host server name
    user = 'root',     #username 
    passwd = 'dwjk7158',
    db = 'crypto')    #database name 

cursor = database.cursor()
cursor.execute("SELECT * FROM users WHERE name = 'joe'")  #SQL commands inserted into CMD.prompt
results = cursor.fetchall()
cursor.close()                                              
print(results)