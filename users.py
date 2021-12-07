from flask import Flask, render_template, request, redirect, url_for, flash
from bson.objectid import ObjectId
import datetime

from database import *
from flask import Blueprint

user_routes = Blueprint('user_routes', __name__)


""" USER PROFILE ROUTE """
# GET Profile page
@user_routes.route('/profile')
def user_profile():

  user = {
    'name': 'Guest User',
    'blabs': blabs.find()
    # Must be blabs by this specific user._id!
    # Comments too if I do that
  }
  return render_template('profile.html', user=user, blabs=blabs.find(), )



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
    user_id = found_user['_id']
    print('found user\'s id:', user_id)
    flash('Successfully logged in!', 'success')
    return redirect(url_for('blab_routes.all_blabs_index', user_id=user_id))
  else:
    flash('User or password incorrect.', 'danger')
    return redirect(url_for('user_routes.login'))



""" LOGOUT """
@user_routes.route('/logout')
def logout():
  print('logout pressed!')
  flash('Successfully logged out!', 'warning')
  return redirect(url_for('blab_routes.all_blabs_index'))



