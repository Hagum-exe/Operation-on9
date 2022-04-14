from flask_mysqldb import MySQLdb


database = MySQLdb.Connect(
    host = 'localhost',
    user = 'root',
    passwd = 'dwjk7158',
    db = 'crypto')

mycursor = database.cursor()

#mycursor.execute('INSERT INTO test1(name, email) VALUES(%s, %s)', ('Tam', 'Tam.email'))
#database.commit()
#mycursor.execute('SELECT * FROM test1')
#mycursor.execute('DESCRIBE test1')
#for x in mycursor:
#   print(x)
    
