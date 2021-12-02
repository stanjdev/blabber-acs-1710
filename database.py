import os
from pymongo import MongoClient

# MONGO_URI is Config Var for Heroku
host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/blabber')
client = MongoClient(host=host)
db = client.get_default_database()

# Blabs resource in our MongoDB
blabs = db.blabs

# Comments resource in our MongoDB
comments = db.comments