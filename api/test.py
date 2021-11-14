
from flask import Flask
from flask_pymongo import PyMongo
import database.database as DB



app = Flask(__name__)
# MONGO URI is used for connecting the app to the mongodb atlas.Copy the connection string from atlas.
# app.config["MONGO_URI"] = "mongodb+srv://m001-student:m001-mongodb-basics@sandbox.ewm7q.mongodb.net/bucket_list?retryWrites=true&w=majority"
app.config["MONGO_URI"] = "mongodb://localhost:27017/bucket_list"
mongo = PyMongo(app)
print("Hello")
# notes = DB.find_some(mongo)

# for note in notes:
# 	print (note['country'])

if __name__ == '__main__':
	app.run(debug=True)