import mysql.connector


SQLdb = mysql.connector.connect(
    user = 'root',
    password = 'dwjk7158',
    host = 'localhost',
    database = 'crypto')    #login to localhost root user


def main():
    from On9SQLhelpers_test import Table, isnewuser
    
    print(isnewuser('on9-joeman'))
   
if __name__ == "__main__":
    main()
    
  