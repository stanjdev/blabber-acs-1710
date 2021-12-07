from flask import Flask, render_template, request, redirect, url_for, flash
from bson.objectid import ObjectId
import datetime

from database import *
from flask import Blueprint

comment_routes = Blueprint('comment_routes', __name__)


""" COMMENTS ROUTES """
# POST a new comment on a specific blab
@comment_routes.route('/blabs/<blab_id>/comments', methods=['POST'])
def comment_new(blab_id):
  now = datetime.datetime.now()
  comment = {
    'blab_id': blab_id,
    'comment_content': request.form.get('comment_content'),
    'date': now
  }
  comments.insert_one(comment)
  flash('Successfully posted a comment!', 'success')
  return redirect(url_for('blab_routes.blab_show_one', blab_id=blab_id))


# GET the edit form for editing one comment
@comment_routes.route('/blabs/<blab_id>/comments/<comment_id>/edit')
def comment_edit_form(blab_id, comment_id):
  blab = blabs.find_one({'_id': ObjectId(blab_id)})
  comment = comments.find_one({'_id': ObjectId(comment_id)})
  return render_template('comment_edit.html', blab=blab, comment=comment, title='Edit Comment')


# PUT/PATCH - UPDATE a comment on a specific blab
@comment_routes.route('/blabs/<blab_id>/comments/<comment_id>', methods=['POST'])
def comment_edit(blab_id, comment_id):
  now = datetime.datetime.now()
  original_comment = comments.find_one({'_id': ObjectId(comment_id)})
  updated_comment = {
    'blab_id': blab_id,
    'comment_content': request.form.get('comment_content'),
    'date': original_comment['date'],
    'updated_date': now,
  }
  comments.update_one(
    {'_id': ObjectId(comment_id)},
    {'$set': updated_comment}
  )
  flash('Successfully edited a comment!', 'info')
  return redirect(url_for('blab_routes.blab_show_one', blab_id=blab_id))


# DELETE - a comment on a specific blab
@comment_routes.route('/blabs/<blab_id>/comments/<comment_id>/delete')
def comment_delete(blab_id, comment_id):
  comments.delete_one({'_id': ObjectId(comment_id)})
  flash('Successfully deleted a comment!', 'warning')
  return redirect(url_for('blab_routes.blab_show_one', blab_id=blab_id))



