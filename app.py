import os
from flask import Flask
from users import user_routes
from comments import comment_routes
from blabs import blab_routes

app = Flask(__name__)
app.register_blueprint(user_routes)
app.register_blueprint(comment_routes)
app.register_blueprint(blab_routes)


if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))

