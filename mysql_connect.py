
import mysql.connector



SQLdb = mysql.connector.connect(
    user = 'root',
    password = 'dwjk7158',
    host = 'localhost',
    database = 'crypto')


def main():
    from sql_functions import Table
    test2 = Table('test2', 'name', 'email')    #initialize 'Table' with 'test2'
    test2.insert('joe', 'joemama.email')
  
if __name__ == "__main__":
    main()
    
    