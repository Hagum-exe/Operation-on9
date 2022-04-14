
import mysql.connector



SQLdb = mysql.connector.connect(
    user = 'root',
    password = 'dwjk7158',
    host = 'localhost',
    database = 'crypto')


def main():
    from sql_functions import Table
    #from sqlhelpers import Table
    users = Table('users', 'name', 'email', 'username', 'password')    #initialize 'Table' with 'users'
    #users.insert('joeman', 'joemanmama.email', 'on9-joeman', 'pw.joemanison9')
    print(users.selectOne('name', 'joe'))
if __name__ == "__main__":
    main()
    
  