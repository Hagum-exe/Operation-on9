
from flask import Flask , render_template, flash, redirect, url_for, session,  request, logging
from passlib.hash import sha256_crypt
from functools import wraps
from forms import *
from On9SQLhelpers import *
def main():
    
   
    
    app = Flask(__name__)  #initialize flask function to start webpage

  


    def loginUser(username):   #login function that gets the details of the user
       users = Table("users", "name", "email", "username", "password")
       
       user = users.selectRow('username', username)
       
       session['logged_in'] = True
       session['username'] = username
       session['name'] = users.selectOneData('name', 'username', username)
       session['email'] = users.selectOneData('email', 'username', username)
       session['balance'] = getBalance(username)
    
    @app.route("/login", methods = ['GET', 'POST'])  #URL and corresponding function for its functions
    def login():
    #if form is submitted
        if request.method == 'POST':        #if button is clicked
        #collect form data
            global loginUsername
            username = request.form['username']  #collect login data
            candidate = request.form['password']

        #access users table to get the user's actual password
            users = Table("users", "name", "email", "username", "password", 'coinmined')
            #user = users.selectRow("username", username)
            accPass = users.selectOneData('password', 'username', username)

        #if the password cannot be found, the user does not exist
            if accPass is None:
                flash("Username is not found", 'danger')   #if have no password
                return redirect('/login')
            
            else:
             #verify that the password entered matches the actual password
                if sha256_crypt.verify(candidate, accPass):
                  #log in the user and redirect to Dashboard page
                    loginUser(username)
                    flash('You are now logged in.', 'success')  #shows data of successfully logging in
                    loginUsername = username
                    return render_template('dashboard.html')    #return the dashboard for the user
                else:
                 #if the passwords do not match
                    flash("Invalid password", 'danger')     #flash message of invalid password
                    return redirect('/login')              #redirects to login page
        return render_template('login.html')  #returns login page
 
    @app.route("/logout")  #logout URL
    def logout(): 
        session.clear()                #clears session and its corresponding data
        flash('Logout Success', 'success')
        return redirect('/login')      #redirects to login page
    
    @app.route("/register", methods = ['GET', 'POST'])  #register page 
    def register():
        form = RegisterForm(request.form)
        users = Table('users', 'name', 'email', 'username', 'password', 'coinmined')
        
        #if form is submitted
        if request.method == 'POST' and form.validate():  #if button is clicked
        
            newusername = form.username.data  #collect form data entered in the webpage
            email = form.email.data
            name = form.name.data
            
            if isnewuser(newusername) == True:  #if user is newuser
            
                password = sha256_crypt.encrypt (form.password.data)   #collect and encrypt password
                users.insert(name, email, newusername, password, '0')     #log to MySQL database
                return redirect('/dashboard')                     #redirect to dashboard page
        
            else:
                flash('User already exists', 'danger')  #if username already exists
                return redirect('/register')            #redirect to register page
        
        return render_template('register.html', form=form)   #return register page
   
    def isLoggedIn(f):              #ensure that user is logged in 
        @wraps(f)
        def wrap(*args, **kwargs):
            if 'logged_in' in session:  #if 'logged_in' message is present in the session
                return f(*args, **kwargs)  #return the webpages
            else:
                flash("Unauthorized, please login.", "danger")   #if user is not logged in
                return redirect(url_for('login'))               #denies access to webpages and redirect to login page
        return wrap
    
    
    #transaction page
    @app.route('/transaction', methods = ['GET', 'POST'])
    @isLoggedIn
    def transaction():
        form = SendMoneyForm(request.form)
        balance = getBalance(session.get('username'))
        
        if request.method == 'POST':
            try: 
                sendMoney(session.get('username'), form.username.data, form.amount.data)
                flash('Money sent, transaction successful', 'success')
            except Exception as e:
                flash(str(e), 'danger')
        
            return redirect('/transaction')
        
        return (render_template('transaction.html', balance=balance, form=form))
      
    #######################################################   
    #buy page
    @app.route('/buy', methods=['GET', 'POST'])
    @isLoggedIn
    def buy():
        form = BuyForm(request.form)
        balance = getBalance(session.get('username'))
        
        if request.method == 'POST':
            try: 
                sendMoney('On9admin', session.get('username'), form.amount.data)
                flash('Purchase Successful', 'success')
            except Exception as e:
                flash(str(e), 'danger')
        
            return redirect('/dashboard')
        
        return render_template('buy.html', balance=balance, form=form)
        
        
    
    #dashboard page
    @app.route("/dashboard")         #dashboard page
    @isLoggedIn                      #ensure that user is logged in
    def dashboard():
        balance = getBalance(session.get('username'))
        return render_template('dashboard.html', session=session)
    
    @app.route("/")                 #main page 
    def index():
        return render_template('index.html')  #renders index.html
   
    ################################################

    app.secret_key = 'the secret key is secret'  #secret key for flask
    app.run(debug=True)  #run app


if __name__ == "__main__":
    main()        #runs main()