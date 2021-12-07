import os
from flask import Flask, render_template, session
from users import user_routes
from comments import comment_routes
from blabs import blab_routes

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.register_blueprint(user_routes)
app.register_blueprint(comment_routes)
app.register_blueprint(blab_routes)

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404


if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))

