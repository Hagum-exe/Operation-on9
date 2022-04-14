from flask_mysqldb import MySQLdb


database = MySQLdb.Connect(
    host = 'localhost',
    user = 'root',
    passwd = 'dwjk7158',
    db = 'crypto')

cursor = database.cursor()
cursor.execute("SELECT * FROM users WHERE name = 'joe'")
results = cursor.fetchall()
cursor.close()
print(results)