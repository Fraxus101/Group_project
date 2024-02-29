from flask_app import app
from flask_app.models.Review import Review
from flask_app.models.User import User

from flask import request , render_template , session , redirect

@app.route('/review/add-review')
def add_review():
    user = User.get_by_id({'id': session['user_id']})
    return render_template('add_review.html', logged_user = user)

@app.route('/review/create' , methods = ['POST'])
def create():
    data = request.form
    Review.create(data)
    return redirect('/dashboard')

@app.route('/review/<int:id>/edit')
def edit_review(id):
    review = Review.get_by_id({'id': id})
    if review.user.id != session['user_id']:
        return redirect('/dashboard')
    return render_template('edit_review.html' , review = review)

@app.route('/review/update' , methods = ['POST'])
def update():
    data = request.form
    Review.update(data)
    return redirect('/dashboard')

@app.route('/review/<int:id>/delete')
def delete(id):
    data = {'id': id}
    review = Review.get_by_id(data)
    if review.user.id == session['user_id']:
        Review.delete(data)
    
    return redirect('/dashboard')

@app.route('/review/<int:id>')
def show(id):
    data = {'id': id}
    review = Review.get_by_id(data)
    return render_template('show_review.html' , review = review)