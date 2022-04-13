import MySQLdb


databse = MySQLdb.Connect(
    host = 'localhost',
    user = 'root',
    passwd = 'dwjk7158',
    db = 'crypto')

mycursor = databse.cursor()

mycursor.execute('INSERT INTO test1(name, email) VALUES(%s, %s)', ('Tim', 'Tim.email'))
databse.commit()
#mycursor.execute('SELECT * FROM test1')

#for x in mycursor:
    #print(x)
    
