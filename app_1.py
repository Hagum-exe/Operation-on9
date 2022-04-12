from flask import Flask, render_template, flash, redirect, url_for, session,  request, logging
from flask_mysqldb import MySQL
import sys
from sqlhelpers import *
from forms import *
#import password
with open('sql_pw.txt') as f:
    pw = f.read()


#import coinlog data of coins
with open('coinlog.txt') as f:
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

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    return render_template('register.html')
    users = Table('users', 'name', 'email', 'username', 'password')

    if request.method == 'POST' and form.validate():
        pass
    return render_template('register.html', form=form)


   
   
   
@app.route("/")
def index():
    return render_template('index.html')
    
if __name__ == "__main__":
    app.secret = 'secret123'
    app.run(debug=True)