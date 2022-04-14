from flask import Flask , render_template, flash, redirect, url_for, session,  request, logging
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL
import mysql.connector
#from functools import wraps

#import other functions and classes
from sqlhelpers import *
from forms import *

#other dependencies
import time

with open('sql_pw.txt') as f:
    pw = f.read()


#import coinlog data of coins
with open('coinlog.txt') as f:
    coinlog = f.read()
#



#initialize the app
app = Flask(__name__)

#configure mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = pw
app.config['MYSQL_DB'] = 'crypto'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#initialize mysql
mysql = MySQLdb.Connect(app)


#Registration page
@app.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    users = Table("users", "name", "email", "username", "password")
    users.insert('test', 'test', 'test', 'test_hash')
    #if form is submitted
    if request.method == 'POST' and form.validate():
        #collect form data
        username = form.username.data
        email = form.email.data
        name = form.name.data

        #make sure user does not already exist
        if isnewuser(username):
            #add the user to mysql and log them in
            password = sha256_crypt.encrypt(form.password.data)
            users.insert(name,email,username,password)
            #log_in_user(username)
            return redirect(url_for('dashboard'))
        else:
            flash('User already exists', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html', form=form)


@app.route("/")
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.secret = 'secret123'
    app.run(debug=True)