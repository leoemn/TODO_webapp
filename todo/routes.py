from todo import app, db, bcrypt
from flask import render_template, flash, redirect, url_for
from todo.forms import LoginForm, RegistrationForm
from todo.models import User, Task

@app.route('/')
def home():

    return render_template('index.html', title = 'Home')
@app.route('/login', methods = ['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        flash('LogIn successful','success')
        return redirect(url_for('home'))

    return render_template('login.html',title = 'LogIn', form = form)

@app.route('/register', methods = ['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username = form.username.data, email = form.email.data, password = hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash('Account was created!', 'success')
        return redirect(url_for('home'))
    
    return render_template('register.html', title = 'Create New Acccount', form = form)
