import mysql.connector
from flask import Flask , render_template, flash, redirect, url_for, session,  request, logging
from passlib.hash import sha256_crypt

from forms import *


#login to mysql locolhost root user

SQLdb = mysql.connector.connect(
    user = 'root',
    password = 'dwjk7158',
    host = 'localhost',
    database = 'crypto')
#


def main():
    
    from On9SQLhelpers import Table, isnewuser
    
    app = Flask(__name__)

    @app.route("/register", methods = ['GET', 'POST'])
    def register():
        form = RegisterForm(request.form)
        users = Table('users', 'name', 'email', 'username', 'password')
        
        
        
        #if form is submitted
        if request.method == 'POST' and form.validate():
        #collect form data
            username = form.username.data
            email = form.email.data
            name = form.name.data
            
            if isnewuser(username) == True:
            
                password = sha256_crypt.encrypt (form.password.data)   #collect and encrypt password
                users.insert(name, email, username, 'PW-Hash')     #log to MySQL database
                return render_template('dashboard.html')
        
            else:
                flash('User already exists', 'danger')
                return render_template('register.html')
        
        return render_template('register.html', form=form)

    
    @app.route("/")
    def index():
        return render_template('index.html')


    
    
    
    
    app.secret_key = 'the secret key is secret'
    app.run(debug=True)  #run app


if __name__ == "__main__":
    main()
    
    