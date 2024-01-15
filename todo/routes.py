import os
import secrets
from PIL import Image
from todo import app, db, bcrypt
from flask import render_template, flash, redirect, url_for, abort,request
from todo.forms import LoginForm, RegistrationForm, AddTaskForm, UpdateTaskForm, UpdateAccountForm
from todo.models import User, Task
from flask_login import current_user,login_user, logout_user,login_required

#Creating a route for homepage
@app.route('/', methods = ['GET','POST'])
@login_required
def home():
    tasks = current_user.tasks
    form = AddTaskForm()

    if form.validate_on_submit():
        new_task = Task(title = form.title.data, description = form.description.data, user_id = current_user.id)

        db.session.add(new_task)
        db.session.commit()

        flash('Task has been created!','success')
        return redirect(url_for('home'))


    return render_template('index.html', title = 'Home', tasks = tasks, form = form)

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

@app.route('/delete_task/<int:task_id>', methods = ['POST'])
@login_required
def delete_task(task_id):
    selected_task = Task.query.get_or_404(task_id)

    #only user who created the task can delete that task     
    if selected_task.author.id != current_user.id:
        abort(403)

    db.session.delete(selected_task)
    db.session.commit()

    flash('Task has been deleted!')
    return redirect(url_for('home'))


@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    selected_task = Task.query.get_or_404(task_id)

    if selected_task.author.id != current_user.id:
        abort(403)

    form = UpdateTaskForm()
    if form.validate_on_submit():    
        selected_task.title = form.title.data
        selected_task.description = form.description.data
        db.session.commit()
        flash('Task has been updated successfully!', 'success')
        return redirect(url_for('home'))

    elif request.method == 'GET':
        form.title.data = selected_task.title
        form.description.data = selected_task.description

    return render_template('edit_task.html', title='Edit Task', form=form, task_id=task_id)

def save_image(form_image):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    image_name = random_hex + f_ext
    image_path = os.path.join(app.root_path, 'static/profile_pics', image_name)
    
    image_size = (125, 125)
    i = Image.open(form_image)
    i.thumbnail(image_size)
    i.save(image_path)

    return image_name

@app.route('/account',methods = ['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        if form.image.data:
            new_image = save_image(form.image.data)
            current_user.profile_pic = new_image
            
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account has been Updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
         
    image_file = url_for('static', filename = 'profile_pics/' + current_user.profile_pic)
    return render_template('account.html', title = 'Account', image_file = image_file, form = form)

#creating route to logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))