from flask import Flask, render_template, flash, redirect, url_for, session,  request, logging

import mysql.connector

app = Flask(__name__)

database = mysql.connector.connect(
    user = 'root',
    password = 'dwjk7158',
    host = 'localhost',
    database = 'crypto')






@app.route("/")
def index():

    

    return render_template('index.html')

if __name__ == "__main__":
   app.secret = 'secret123'
   app.run(debug=True)

    




