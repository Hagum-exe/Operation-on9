
from flask import Flask , render_template, flash, redirect, url_for, session,  request, logging
from passlib.hash import sha256_crypt
from functools import wraps
from forms import *
from On9SQLhelpers import *
def main():
    
    from On9SQLhelpers import Table, isnewuser
    
    app = Flask(__name__)

    
    
    
    def loginUser(username):
       users = users = Table("users", "name", "email", "username", "password", 'coinmined')
       
       user = users.selectRow('username', username)
       
       session['logged_in'] = True
       session['username'] = username
       session['name'] = users.selectOneData('name', 'username', username)
       session['email'] = users.selectOneData('email', 'username', username)
       #session['coinmined'] = users
    @app.route("/login", methods = ['GET', 'POST'])
    def login():
    #if form is submitted
        if request.method == 'POST':
        #collect form data
            username = request.form['username']
            candidate = request.form['password']

        #access users table to get the user's actual password
            users = Table("users", "name", "email", "username", "password", 'coinmined')
            #user = users.selectRow("username", username)
            accPass = users.selectOneData('password', 'username', username)

        #if the password cannot be found, the user does not exist
            if accPass is None:
                flash("Username is not found", 'danger')
                return redirect('/login')
            else:
             #verify that the password entered matches the actual password
                if sha256_crypt.verify(candidate, accPass):
                  #log in the user and redirect to Dashboard page
                    loginUser(username)
                    flash('You are now logged in.', 'success')
                    return render_template('dashboard.html')
                else:
                 #if the passwords do not match
                    flash("Invalid password", 'danger')
                    return redirect('/login')
        return render_template('login.html')
 
    @app.route("/logout")
    def logout():
        session.clear()
        flash('Logout Success', 'success')
        return redirect('/login')
    
    @app.route("/register", methods = ['GET', 'POST'])
    def register():
        form = RegisterForm(request.form)
        users = Table('users', 'name', 'email', 'username', 'password', 'coinmined')
        
        
        
        #if form is submitted
        if request.method == 'POST' and form.validate():
        #collect form data
            username = form.username.data
            email = form.email.data
            name = form.name.data
            
            if isnewuser(username) == True:
            
                password = sha256_crypt.encrypt (form.password.data)   #collect and encrypt password
                users.insert(name, email, username, password)     #log to MySQL database
                return redirect('/dashboard')
        
            else:
                flash('User already exists', 'danger')
                return redirect('/register')
        
        return render_template('register.html', form=form)
   
    def isLoggedIn(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            if 'logged_in' in session:
                return f(*args, **kwargs)
            else:
                flash("Unauthorized, please login.", "danger")
                return redirect(url_for('login'))
        return wrap
    
    
    @app.route("/dashboard")
    #@isLoggedIn
    def dashboard():
        return render_template('dashboard.html', session=session)
    
    
    
    @app.route("/mine", methods = ['GET', 'POST'])
    @isLoggedIn
    def mine():
        from On9blockchain import main
     
        if request.method == 'POST':
            amount = int(request.form['amount'])
            main(amount)
            return redirect("dashboard")
        return render_template('mine.html')   
    
    
    @app.route("/")
    def index():
        return render_template('index.html')


    app.secret_key = 'the secret key is secret'
    app.run(debug=True)  #run app


if __name__ == "__main__":
    main()