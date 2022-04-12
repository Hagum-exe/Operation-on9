#!/usr/bin/python
# -*- coding: utf-8 -*-

#import flask dependencies for web GUI
from flask import Flask, render_template, flash, redirect, url_for, session,  request, logging
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL
from functools import wraps

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
mysql = MySQL(app)

#wrap to define if the user is currently logged in from session
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("Unauthorized, please login.", "danger")
            return redirect(url_for('login'))
    return wrap

#log in the user by updating session
def log_in_user(username):
    users = Table("users", "name", "email", "username", "password")
    user = users.getone("username", username)

    session['logged_in'] = True
    session['username'] = username
    session['name'] = user.get('name')
    session['email'] = user.get('email')

#Registration page
@app.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    users = Table("users", "name", "email", "username", "password")

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
            log_in_user(username)
            return redirect(url_for('dashboard'))
        else:
            flash('User already exists', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html', form=form)