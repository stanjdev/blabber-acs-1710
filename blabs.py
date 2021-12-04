import pymongo
from flask import Flask, render_template, request, redirect, url_for
from bson.objectid import ObjectId
import datetime

from database import *
from flask import Blueprint

blab_routes = Blueprint('blab_routes', __name__)


""" BLABS - RESTFUL ROUTES """
# GET - INDEX ROOT Route - HOME PAGE, ALL BLABS
@blab_routes.route('/')
def all_blabs_index():
  return render_template('all_blabs_index.html', blabs=blabs.find())

# GET - SHOW a specific blab from blab._id
@blab_routes.route('/blabs/<blab_id>')
def blab_show_one(blab_id):
  blab = blabs.find_one({'_id': ObjectId(blab_id)})
  blab_comments = comments.find({'blab_id': blab_id})
  return render_template('blab_show_one.html', blab=blab, comments=blab_comments)

# GET - form to add NEW blab
@blab_routes.route('/blabs/new')
def new_blab():
  blab = {}
  return render_template('blabs_new.html', title='New Blab', blab=blab) 

# POST - CREATE / SUBMIT a blab
@blab_routes.route('/blabs', methods=['POST'])
def blab_submit():
  now = datetime.datetime.now()
  # print(now.strftime("%m-%d-%Y %H:%M"))
  blab = {
    'text_content': request.form.get('text_content'),
    'date': now,
  }
  # WRITES TO THE blabs DB
  blabs.insert_one(blab)

  return redirect(url_for('blab_routes.all_blabs_index'))

# GET - EDIT form
@blab_routes.route('/blabs/<blab_id>/edit')
def blab_edit_page(blab_id):
  blab = blabs.find_one({'_id': ObjectId(blab_id)})
  return render_template('blabs_edit.html', blab=blab, title='Edit Blab')

# PUT/PATCH - UPDATE a blab
@blab_routes.route('/blabs/<blab_id>', methods=['POST'])
def blab_update(blab_id):
  # The newly updated form data
  now = datetime.datetime.now()
  original_blab = blabs.find_one({'_id': ObjectId(blab_id)})
  
  updated_blab = {
    'text_content': request.form.get('text_content'),
    'date': original_blab['date'],
    'updated_date': now
  }
  # Set that former blab from db to this updated one
  blabs.update_one(
    {'_id': ObjectId(blab_id)},
    {'$set': updated_blab}
  )
  return redirect(url_for('blab_routes.all_blabs_index'))

# DELETE - a blab 
# USING AN <a> TAG WITHOUT POST METHOD WORKS
@blab_routes.route('/blabs/<blab_id>/delete')
def donations_delete(blab_id):
  blabs.delete_one({'_id': ObjectId(blab_id)})
  return redirect(url_for('blab_routes.all_blabs_index'))



