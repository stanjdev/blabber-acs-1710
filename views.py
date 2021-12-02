import pymongo
from flask import Flask, render_template, request, redirect, url_for
from bson.objectid import ObjectId
import datetime

from database import *
from flask import Blueprint

routes = Blueprint('routes', __name__)



""" BLABS - RESTFUL ROUTES """

# GET - INDEX ROOT Route - HOME PAGE, ALL BLABS
@routes.route('/')
def all_blabs_index():
  return render_template('all_blabs_index.html', blabs=blabs.find())

# GET - SHOW a specific blab from blab._id
@routes.route('/blabs/<blab_id>')
def blab_show_one(blab_id):
  blab = blabs.find_one({'_id': ObjectId(blab_id)})
  blab_comments = comments.find({'blab_id': blab_id})
  return render_template('blab_show_one.html', blab=blab, comments=blab_comments)

# GET - form to add NEW blab
@routes.route('/blabs/new')
def new_blab():
  blab = {}
  return render_template('blabs_new.html', title='New Blab', blab=blab) 

# POST - CREATE / SUBMIT a blab
@routes.route('/blabs', methods=['POST'])
def blab_submit():
  now = datetime.datetime.now()
  # print(now.strftime("%m-%d-%Y %H:%M"))
  blab = {
    'text_content': request.form.get('text_content'),
    'date': now,
  }
  # WRITES TO THE blabs DB
  blabs.insert_one(blab)

  return redirect(url_for('routes.all_blabs_index'))

# GET - EDIT form
@routes.route('/blabs/<blab_id>/edit')
def blab_edit_page(blab_id):
  blab = blabs.find_one({'_id': ObjectId(blab_id)})
  return render_template('blabs_edit.html', blab=blab, title='Edit Blab')

# PUT/PATCH - UPDATE a blab
@routes.route('/blabs/<blab_id>', methods=['POST'])
def blab_update(blab_id):
  # The newly updated form data
  now = datetime.datetime.now()
  updated_blab = {
    'text_content': request.form.get('text_content'),
    'date': now,
  }
  # Set that former blab from db to this updated one
  blabs.update_one(
    {'_id': ObjectId(blab_id)},
    {'$set': updated_blab}
  )
  return redirect(url_for('routes.all_blabs_index'))

# DELETE - a blab 
# USING AN <a> TAG WITHOUT POST METHOD WORKS
@routes.route('/blabs/<blab_id>/delete')
def donations_delete(blab_id):
  blabs.delete_one({'_id': ObjectId(blab_id)})
  return redirect(url_for('routes.all_blabs_index'))








""" USER PROFILE ROUTE """

# GET Profile page
@routes.route('/profile')
def user_profile():

  user = {
    'name': 'Guest User',
    'blabs': blabs.find()
    # Must be blabs by this specific user._id!
    # Comments too if I do that
  }
  return render_template('profile.html', user=user, blabs=blabs.find(), )







""" COMMENTS ROUTES """
# POST a new comment on a specific blab
@routes.route('/blabs/<blab_id>/comments', methods=['POST'])
def comment_new(blab_id):
  now = datetime.datetime.now()
  comment = {
    'blab_id': blab_id,
    'comment_content': request.form.get('comment_content'),
    'date': now
  }
  comments.insert_one(comment)
  return redirect(url_for('routes.blab_show_one', blab_id=blab_id))


# GET the edit form for editing one comment
@routes.route('/blabs/<blab_id>/comments/<comment_id>/edit')
def comment_edit_form(blab_id, comment_id):
  blab = blabs.find_one({'_id': ObjectId(blab_id)})
  comment = comments.find_one({'_id': ObjectId(comment_id)})
  return render_template('comment_edit.html', blab=blab, comment=comment, title='Edit Comment')


# PUT/PATCH - UPDATE a comment on a specific blab
@routes.route('/blabs/<blab_id>/comments/<comment_id>', methods=['POST'])
def comment_edit(blab_id, comment_id):
  now = datetime.datetime.now()
  updated_comment = {
    'blab_id': blab_id,
    'comment_content': request.form.get('comment_content'),
    'date': now
  }
  comments.update_one(
    {'_id': ObjectId(comment_id)},
    {'$set': updated_comment}
  )
  return redirect(url_for('routes.blab_show_one', blab_id=blab_id))



# DELETE - a comment on a specific blab
@routes.route('/blabs/<blab_id>/comments/<comment_id>/delete')
def comment_delete(blab_id, comment_id):
  comments.delete_one({'_id': ObjectId(comment_id)})
  return redirect(url_for('routes.blab_show_one', blab_id=blab_id))








""" LOGIN ROUTES """

# GET login page
@routes.route('/login')
def login_form():
  return render_template('login.html')

# POST to log user in
@routes.route('/login', methods=['POST'])
def login():
  user = {
    'email': request.form.get('email'),
    'password': request.form.get('password')
  }
  print(user)
  return render_template('donations_new.html')

# GET sign up page
@routes.route('/signup')
def signup_form():
  return render_template('signup.html')

# POST to register new user
@routes.route('/signup', methods=['POST'])
def signup():
  new_user = {
    'email': request.form.get('email'),
    'password': request.form.get('password'),
    'confirm_password': request.form.get('confirm_password'),
  }
  print(new_user)
  return render_template('login.html')





