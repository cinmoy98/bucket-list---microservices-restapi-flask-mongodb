from flask import Flask, jsonify, request, redirect, render_template 
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import json
from bson import BSON
from bson import json_util
import shortuuid
from models.notes import Note

app = Flask(__name__)
# MONGO URI is used for connecting the app to the mongodb atlas.Copy the connection string from atlas.
# app.config["MONGO_URI"] = "mongodb+srv://m001-student:m001-mongodb-basics@sandbox.ewm7q.mongodb.net/bucket_list?retryWrites=true&w=majority"
app.config["MONGO_URI"] = "mongodb://localhost:27017/bucket_list"
mongo = PyMongo(app)


@app.route('/create_note_test',methods=['POST'])
def create_note_test():

	uid = request.form['userid']
	title = request.form['title']
	description = request.form['description']
	category = request.form.getlist('category[]')
	country = request.form['country']
	city = request.form['city']
	yt_link = request.form.getlist('youtube[]')
	fb_link = request.form.getlist('facebook[]')
	blog_link = request.form.getlist('blog[]')
	insta_link = request.form.getlist('instagram[]')
	gmap = request.form['gmap']

	new_note = Note(uid, title, description, category, country, city, yt_link, fb_link, blog_link, insta_link,gmap )
	new_note.save_it(mongo)
	return "Created !"


if __name__ == '__main__':
	app.run(debug=True)
