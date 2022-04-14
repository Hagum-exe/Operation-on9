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
        #users = Table('users', 'name', 'email', 'username', 'password')    #initialize 
        #'Table' with 'users'
        
        users = Table('users', 'name', 'email', 'username', 'password')
        
        
        
        #if form is submitted
        if request.method == 'POST' and form.validate():
        #collect form data
            username = form.username.data
            email = form.email.data
            name = form.name.data
            users.insert(name, email, username, 'PW-Hash')
            #make sure user does not already exist
            return render_template('dashboard.html')
        return render_template('register.html', form=form)

    
    @app.route("/")
    def index():
        return render_template('index.html')


    
    
    
    
    
    app.run(debug=True)  #run app


if __name__ == "__main__":
    main()
    
    