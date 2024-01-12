from todo import app, db, bcrypt
from flask import render_template, flash, redirect, url_for
from todo.forms import LoginForm, RegistrationForm
from todo.models import User, Task
from flask_login import current_user,login_user, logout_user,login_required

#Creating a route for homepage
@app.route('/')
def home():

    return render_template('index.html', title = 'Home')

#Creating a route for login page
@app.route('/login', methods = ['GET','POST'])
def login():
    #We dont want users to go on login page if they already logged in
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit():
        #we get the user from database using email provided in our LoginForm by user
        user = User.query.filter_by(email = form.email.data).first()

        #checking if we have the user with the email and if pasword is correct
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            flash('LogIn successful','success')
            return redirect(url_for('home'))
        else:
            flash('Please check your email and password!', 'danger')

    return render_template('login.html',title = 'LogIn', form = form)


#Creating route for registration page
@app.route('/register', methods = ['GET','POST'])
def register():
    #We dont want users to go on login page if they already logged in
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()

    if form.validate_on_submit():
        #genrating hashed password to save in our database
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        #adding user to our database
        new_user = User(username = form.username.data, email = form.email.data, password = hashed_pw)

        db.session.add(new_user)
        db.session.commit()

        flash('Account was created!', 'success')
        return redirect(url_for('home'))
    
    
    return render_template('register.html', title = 'Create New Acccount', form = form)

#creating route to logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))