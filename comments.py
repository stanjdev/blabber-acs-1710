from flask import Flask, render_template, request, redirect, url_for, flash, session
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
  if 'user_id' in session:
    comment = {
      'blab_id': blab_id,
      'comment_content': request.form.get('comment_content'),
      'date': now,
      'user_id': session['user_id'],
      'user_email': session['email'],
    }
  else:
    comment = {
      'blab_id': blab_id,
      'comment_content': request.form.get('comment_content'),
      'date': now,
      'user_id': 'guest',
      'user_email': 'guest',
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
  if 'user_id' in session:
    if session['user_id'] == original_comment['user_id']:
      updated_comment = {
        'blab_id': blab_id,
        'comment_content': request.form.get('comment_content'),
        'date': original_comment['date'],
        'updated_date': now,
        'user_id': session['user_id'] if session['user_id'] else 'guest',
        'user_email': session['email'] if session['email'] else 'guest'
      }
      comments.update_one(
        {'_id': ObjectId(comment_id)},
        {'$set': updated_comment}
      )
      flash('Successfully edited a comment!', 'info')
      return redirect(url_for('blab_routes.blab_show_one', blab_id=blab_id))
  elif 'user_id' not in session and original_comment['user_id'] == 'guest':
    updated_comment = {
      'blab_id': blab_id,
      'comment_content': request.form.get('comment_content'),
      'date': original_comment['date'],
      'updated_date': now,
      'user_id': 'guest',
      'user_email': 'guest'
    }
    comments.update_one(
      {'_id': ObjectId(comment_id)},
      {'$set': updated_comment}
    )
    flash('Successfully edited a guest comment!', 'info')
    return redirect(url_for('blab_routes.blab_show_one', blab_id=blab_id))
  flash('You can only edit your own comments!', 'danger')
  return redirect(url_for('blab_routes.blab_show_one', blab_id=blab_id))

# DELETE - a comment on a specific blab
@comment_routes.route('/blabs/<blab_id>/comments/<comment_id>/delete')
def comment_delete(blab_id, comment_id):
  comment = comments.find_one({'_id': ObjectId(comment_id)})
  if 'user_id' in session:
    if session['user_id'] == comment['user_id']:
      comments.delete_one({'_id': ObjectId(comment_id)})
      flash('Successfully deleted a comment!', 'warning')
    else:
      flash('You can only delete your own comment.', 'danger')
  elif 'user_id' not in session and comment['user_id'] == 'guest':
    comments.delete_one({'_id': ObjectId(comment_id)})
    flash('Successfully deleted a comment!', 'warning')
  else:
    flash('You can only delete your own comment.', 'danger')
  return redirect(url_for('blab_routes.blab_show_one', blab_id=blab_id))



