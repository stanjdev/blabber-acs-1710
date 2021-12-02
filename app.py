from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
import datetime


from flask import Blueprint
routes = Blueprint('routes', __name__)


# MONGO_URI is Config Var for Heroku
host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/blabber')
client = MongoClient(host=host)

db = client.get_default_database()

# Blabs resource in our MongoDB
blabs = db.blabs

# Comments resource in our MongoDB
comments = db.comments

app = Flask(__name__)


# Donations resource in our MongoDB
donations = db.donations

# Charities resource in our MongoDB
charities = db.charities






""" BLABS - RESTFUL ROUTES """

# GET - INDEX ROOT Route - HOME PAGE, ALL BLABS
@app.route('/')
def all_blabs_index():
  return render_template('all_blabs_index.html', blabs=blabs.find())

# GET - SHOW a specific blab from blab._id
@app.route('/blabs/<blab_id>')
def blab_show_one(blab_id):
  blab = blabs.find_one({'_id': ObjectId(blab_id)})
  return render_template('blab_show_one.html', blab=blab)

# GET - form to add NEW blab
@app.route('/blabs/new')
def new_blab():
  blab = {}
  return render_template('blabs_new.html', title='New Blab', blab=blab, blabs=blabs.find()) 

# POST - CREATE / SUBMIT a blab
@app.route('/blabs', methods=['POST'])
def blab_submit():
  now = datetime.datetime.now()
  # print(now.strftime("%m-%d-%Y %H:%M"))
  blab = {
    'text_content': request.form.get('text_content'),
    'date': now,
  }
  # WRITES TO THE blabs DB
  blabs.insert_one(blab)

  return redirect(url_for('all_blabs_index'))

# GET - EDIT form
@app.route('/blabs/<blab_id>/edit')
def blab_edit_page(blab_id):
  blab = blabs.find_one({'_id': ObjectId(blab_id)})
  return render_template('blabs_edit.html', blab=blab, title='Edit Blab', blabs=blabs.find())

# PUT/PATCH - UPDATE a blab
@app.route('/blabs/<blab_id>', methods=['POST'])
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

  return redirect(url_for('all_blabs_index'))

# DELETE - a blab 
# USING AN <a> TAG WITHOUT POST METHOD WORKS
@app.route('/blabs/<blab_id>/delete')
def donations_delete(blab_id):
  blabs.delete_one({'_id': ObjectId(blab_id)})
  return redirect(url_for('all_blabs_index'))











""" USER PROFILE ROUTE """

# GET Profile page
@app.route('/profile')
def user_profile():

  user = {
    'name': 'Guest User',
    'blabs': blabs.find()
    # Must be blabs by this specific user._id!
    # Comments too if I do that
  }
  return render_template('profile.html', user=user, blabs=blabs.find(), )







""" COMMENTS ROUTES """



""" CHARITIES ROUTES """

# GET ALL Charities /charities
@app.route('/charities')
def charities_all():
  return render_template('charities_all.html', charities=charities.find())


# GET SHOW one Charity profile page
# GET — /charities:/charity_name — SHOW one charity {k: v}
@app.route('/charities/<charity_name>')
def charity_profile(charity_name):
  charity = charities.find_one({'name': charity_name})
  return render_template('charity.html', charity=charity, donations=donations.find({'charity_name': charity_name}))

# # POST - /charities create a new charity when a new one is entered in the donation form
# ADDING A NEW DONATION CREATES ONE ALREADY.


# GET - EDIT form for charity
@app.route('/charities/<charity_name>/edit')
def charity_edit_form(charity_name):
  charity = charities.find_one({'name': charity_name})
  # get the charity object with the info to put in 'value' in each input
  return render_template('charity_edit_form.html', charity=charity)


# PUT/PATCH - UPDATE charity information
@app.route('/charities/<charity_name>', methods=['POST'])
def charities_update(charity_name):
  updated_charity = {
    'name': request.form.get('charity_name'),
    'category': request.form.get('charity_category'),
    'about': request.form.get('about_charity')
  }
  charities.update_one(
    {'name': charity_name},
    {'$set': updated_charity}
  )
  return redirect(url_for('charity_profile', charity_name=updated_charity['name']))


# DELETE a charity
@app.route('/charities/<charity_name>/delete')
def charity_delete(charity_name):
  print(charity_name)
  charities.delete_one({'name': charity_name})
  return redirect(url_for('charities_all'))





""" LOGIN ROUTES """

# GET login page
@app.route('/login')
def login_form():
  return render_template('login.html')

# POST to log user in
@app.route('/login', methods=['POST'])
def login():
  user = {
    'email': request.form.get('email'),
    'password': request.form.get('password')
  }
  print(user)
  return render_template('donations_new.html')

# GET sign up page
@app.route('/signup')
def signup_form():
  return render_template('signup.html')

# POST to register new user
@app.route('/signup', methods=['POST'])
def signup():
  new_user = {
    'email': request.form.get('email'),
    'password': request.form.get('password'),
    'confirm_password': request.form.get('confirm_password'),
  }
  print(new_user)
  return render_template('login.html')








if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))

