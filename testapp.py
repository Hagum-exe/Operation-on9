from flask import Flask, render_template, flash, redirect, url_for, session,  request, logging
import MySQLdb
from sqlhelpers import *
#import password
with open('sql_pw.txt') as f:
    pw = f.read()



    
#print(coinlog)    

app = Flask(__name__)

mysql = MySQLdb.Connect(
    host = 'localhost',
    user = 'root',
    passwd = 'dwjk7158',
    db = 'crypto')




users = Table('users', 'name', 'email', 'username', 'password')
users.insert('hagum', 'hagum@gmail.com', 'hagum', 'hash')
    

@app.route("/")
def index():
    
    
    return render_template('index.html')
    
if __name__ == "__main__":
    app.secret = 'secret123'
    app.run(debug=True)


