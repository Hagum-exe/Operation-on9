import mysql.connector


SQLdb = mysql.connector.connect(
    user = 'root',
    password = 'dwjk7158',
    host = 'localhost',
    database = 'crypto')    #login to localhost root user


def main():
    #from On9SQLhelpers_test import Table
   
    #users = Table('users', 'name', 'email', 'username', 'password')    #initialize 'Table' with 'users'
    #print(users.selectOne('name', 'joe'))
    name = str(input('Enter your name'))
    cursor = SQLdb.cursor()
    #cursor.execute('CREATE TABLE userTest2(user varchar(20),gmail varchar(20),password varchar(20))')
    cursor.execute('INSERT INTO userTest2(user,gmail,password) VALUES("%s", "joshuakwongty2","joshua123452")'%name)
    SQLdb.commit()
    cursor.close()
    
    cursor = SQLdb.cursor()
    cursor.execute('SELECT * FROM userTest2')
    data = cursor.fetchall()  # take everything
    for x in data:
        print(x)
    cursor.close()
   
   
if __name__ == "__main__":
    main()
    
  