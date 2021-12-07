from flask import Flask, render_template, request, redirect, url_for, flash, session
from bson.objectid import ObjectId
import datetime

from database import *
from flask import Blueprint

user_routes = Blueprint('user_routes', __name__)


""" USER PROFILE ROUTE """
# GET Profile page
@user_routes.route('/profile/<user_id>')
def user_profile(user_id):
  if user_id == 'guest':
    user = {
      'email': 'guest',
      'blabs': blabs.find({'user_id': 'guest'}),
      'user_id': 'guest',
      'comments': comments.find({'user_id': 'guest'}),
    }
  else: 
    found_user = users.find_one({'_id': ObjectId(user_id)})
    user = {
        'email': found_user['email'],
        'blabs': blabs.find({'user_id': user_id}),
        'user_id': user_id,
        'comments': comments.find({'user_id': user_id}),
      }
  return render_template('profile.html', user=user, blabs=user['blabs'], comments=user['comments'], all_blabs=blabs.find())



""" SIGNUP ROUTES """
# GET sign up page
@user_routes.route('/signup')
def signup_form():
  return render_template('signup.html')

# POST to register new user
@user_routes.route('/signup', methods=['POST'])
def signup():
  new_user = {
    'email': request.form.get('email'),
    'password': request.form.get('password'),
    'confirm_password': request.form.get('confirm_password'),
  }

  if new_user['password'] != new_user['confirm_password']:
    flash('Passwords do not match!', 'danger')
    return redirect(url_for('user_routes.signup'))
  else:
    users.insert_one(new_user)
    print('New user inserted!', new_user)
    flash('New user successfully created!', 'success')
    return redirect(url_for('user_routes.login'))




""" LOGIN ROUTES """
# GET login page
@user_routes.route('/login')
def login_form():
  print(session)
  return render_template('login.html')

# POST to log user in
@user_routes.route('/login', methods=['POST'])
def login():
  user_input = {
    'email': request.form.get('email'),
    'password': request.form.get('password')
  }
  
  found_user = users.find_one({'email': user_input['email'], 'password':user_input['password']})
  if (found_user):
    session['user_id'] = str(found_user['_id'])
    session['email'] = user_input['email']
    flash('Successfully logged in!', 'success')
    return render_template('all_blabs_index.html', blabs=blabs.find())
  else:
    flash('Email or password incorrect.', 'danger')
    return redirect(url_for('user_routes.login'))



""" LOGOUT """
@user_routes.route('/logout')
def logout():
  session.pop('user_id', None)
  session.pop('email', None)
  print('logout pressed!')
  flash('You have been logged out!', 'warning')
  return redirect(url_for('blab_routes.all_blabs_index'))



