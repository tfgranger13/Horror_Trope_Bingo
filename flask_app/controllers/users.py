from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.user import User

#bcrypt for password hashing
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return redirect('/game')

#route to register a new user
@app.route('/register', methods = ['POST'])
def register():
    data = {
        'first_name': request.form['reg_first_name'],
        'last_name': request.form['reg_last_name'],
        'email': request.form['reg_email'],
        'password': request.form['reg_password']
    }
    reg_confirm_password = request.form['reg_confirm_password']
    if not User.validate_reg_info(data, reg_confirm_password):
        return redirect('/')
    else:
        data['password'] = bcrypt.generate_password_hash(data['password'])
        user_id = User.add_to_db(data)
        session['user_id'] = user_id
        user_name = User.get_single_user(data = {'id': user_id})
        session['user_name'] = f"{user_name.first_name} {user_name.last_name}"
        flash('User registration successful!', 'logging')
    return redirect('/success')

#route to log in if already registered
@app.route('/log_in', methods = ['POST'])
def log_in():
    data = {'email': request.form['login_email']}
    if len(User.check_db_for_reg_email(data)) == 0:
        flash("I'm sorry, there is no user with that email address. Please register before logging in.", "logging")
        return redirect('/')
    user_in_db = User.get_user_by_email(data)
    if not bcrypt.check_password_hash(user_in_db.password, request.form['login_password']):
        flash("Login information is incorrect.", "logging")
        return redirect('/')
    else:
        session['user_id'] = user_in_db.id
        session['user_name'] = f"{user_in_db.first_name} {user_in_db.last_name}"
        return redirect('/success')

#route to the success page
@app.route('/success')
def success():
    if 'user_id' not in session:
        flash("I'm sorry, you must be logged in to view that page.", "logging")
        return redirect('/')
    all_users = User.get_all_users()
    return render_template('success.html', all_users = all_users)

#route to log out a user
@app.route('/log_out')
def log_out():
    if 'user_id' in session:
        session.clear()
        flash("You have been logged out.", "logging")
    else:
        flash("You are not logged in.", "logging")
    return redirect('/')