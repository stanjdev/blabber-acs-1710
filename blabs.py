from flask import Flask, render_template, request, redirect, url_for, flash, session
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

  if 'user_id' in session:
    blab = {
      'text_content': request.form.get('text_content'),
      'date': now,
      'user_id': session['user_id'],
      'user_email': session['email'],
    }
  else:
    blab = {
      'text_content': request.form.get('text_content'),
      'date': now,
      'user_id': 'guest',
      'user_email': 'guest'
    }
  # WRITES TO THE blabs DB
  blabs.insert_one(blab)

  flash('Successfully posted a blab!', 'success')
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

  if 'user_id' in session:
    if original_blab['user_id'] == session['user_id']:
      updated_blab = {
        'text_content': request.form.get('text_content'),
        'date': original_blab['date'],
        'updated_date': now,
        'user_id': session['user_id'],
        'user_email': session['email'],
      }
      # Set that former blab from db to this updated one
      blabs.update_one(
        {'_id': ObjectId(blab_id)},
        {'$set': updated_blab}
      )
      flash('Successfully edited blab!', 'info')
      return redirect(url_for('blab_routes.all_blabs_index')) 

  elif 'user_id' not in session and original_blab['user_id'] == 'guest':
    updated_blab = {
      'text_content': request.form.get('text_content'),
      'date': original_blab['date'],
      'updated_date': now,
      'user_id': 'guest',
      'user_email': 'guest',
    }
    # Set that former blab from db to this updated one
    blabs.update_one(
      {'_id': ObjectId(blab_id)},
      {'$set': updated_blab}
    )
    flash('Successfully edited guest blab!', 'info')
    return redirect(url_for('blab_routes.all_blabs_index')) 
  flash('You can only edit your own blabs!', 'danger')
  return redirect(url_for('blab_routes.blab_show_one', blab_id=blab_id))

# DELETE - a blab 
# USING AN <a> TAG WITHOUT POST METHOD WORKS
@blab_routes.route('/blabs/<blab_id>/delete')
def blabs_delete(blab_id):
  blab = blabs.find_one({'_id': ObjectId(blab_id)})
  if 'user_id' in session:
    if blab['user_id'] == session['user_id']:
      blabs.delete_one({'_id': ObjectId(blab_id)})
      flash('Successfully deleted a blab.', 'warning')
    else:
      flash('You can only delete your own blabs.', 'danger')
  elif 'user_id' not in session and blab['user_id'] == 'guest':
    blabs.delete_one({'_id': ObjectId(blab_id)})
    flash('Successfully deleted a blab.', 'warning')
  else: 
    flash('You can only delete your own blabs.', 'danger')
  return redirect(url_for('blab_routes.all_blabs_index'))



