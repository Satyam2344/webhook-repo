from flask import Flask
import pymongo

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

database_connection = app.config['DB_HOST']
database_name = app.config['DB_NAME']
collection_name  = app.config['COLLECTION_NAME']
users_collection_name = app.config['USERS_COLLECTION_NAME']

# Setup MongoDB here
mongoDB_clint = pymongo.MongoClient(database_connection)
databaseName = mongoDB_clint[database_name]
collectionName = databaseName[collection_name]
usersCollectionName = databaseName[users_collection_name]


