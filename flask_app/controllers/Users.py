from flask_app import app
from flask_app.models.User import User
from flask_app.models.Review import Review

from flask import render_template , request, redirect, session


@app.route('/')
def login_registration():
    if 'user_id' in session: 
        return redirect('/dashboard')
    return render_template('login_registration.html')


@app.route('/register' , methods = ['POST'])
def register():
    data = request.form
    if User.validate_register(data):
        User.register(data)
    return redirect('/')

@app.route('/login' , methods = ['POST'])
def login():
    data = request.form
    if User.validate_login(data):
        user = User.get_by_email(data)
        session['user_id'] = user.id
        return redirect('/dashboard')
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if not 'user_id' in session:
        return redirect('/')
    user_data = {'id': session['user_id']}
    user = User.get_by_id(user_data)
    reviews = Review.get_all()
    return render_template('dashboard.html' , logged_user = user , reviews = reviews)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')