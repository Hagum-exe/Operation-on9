from flask import Flask, render_template, flash, redirect, url_for, session,  request, logging
from flask_mysqldb import MySQL
import sys

#import password
with open('sql_pw.txt') as f:
    pw = f.read()


#import coinlog data of coins
with open('coinlog_on9venv.txt') as f:
    coinlog = f.read()
#

    
#print(coinlog)    

app = Flask(__name__)

# Required
app.config["MYSQL_HOST"] = 'localhost'
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = pw
app.config["MYSQL_DB"] = "crypto"
# Extra configs, optional:
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@app.route("/")
def index():
    return render_template('index.html')
    
if __name__ == "__main__":
    app.secret = 'secret123'
    app.run(debug=True)