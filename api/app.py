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




@app.route('/getnotes',methods=['GET'])
def get_notes():
	notes = Note.find_all_notes(mongo)
	return jsonify(notes)




# getnote recieves _id of a particular note and fetch that note.
@app.route('/getnote/<string:note_id>',methods=['GET'])
def get_note(note_id):
	note = Note.find_by_note_id(note_id, mongo)
	print(note['title'])
	return jsonify(note)



@app.route('/get_category/<string:catg>',methods=['GET'])
def get_category(catg):
	notes = Note.find_by_category(catg, mongo)
	return jsonify(notes)


@app.route('/get_country/<string:country>', methods=['GET'])
def get_country(country):
	notes = Note.find_by_country(country, mongo)
	return jsonify(notes)



@app.route('/get_city/<string:city>', methods=['GET'])
def get_city(city):
	notes = Note.find_by_city(city, mongo)
	return jsonify(notes)



@app.route('/get_cities/<string:country>', methods=['GET'])
def get_cities(country):
	db_ops = mongo.db.buckets

	cities = db_ops.distinct("city", {"country" : country})
	#output = [{city['city']} for city in cities]
	return jsonify(cities)


@app.route('/get_countries/<string:uid>',methods=['GET'])
def get_countries(uid):
	db_ops = mongo.db.buckets

	countries = db_ops.distinct("country")
	return jsonify(countries)



@app.route('/update_note/<note_id>',methods=['POST'])
def update_note(note_id):
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

	update_note = Note(uid, title, description, category, country, city, yt_link, fb_link, blog_link, insta_link,gmap, note_id)
	update_note.update_it(note_id, mongo)
	return "Updated !"



@app.route('/delete_note/<note_id>',methods=['POST'])
def delete_note(note_id):
	Note.delete_note_by_id(note_id, mongo)
	return "Deleted !"


@app.route('/add_yt_link/<note_id>', methods=['POST'])
def add_yt_link(note_id):
	new_yt_link = request.form['youtube']
	mongo.db.test.update({'_id' : note_id}, { '$addToSet' : {'yt_link' : new_yt_link}})
	return "Youtube link added !"


@app.route('/add_fb_link/<note_id>', methods=['POST'])
def add_fb_link(note_id):
	new_fb_link = request.form['facebook']
	mongo.db.test.update({'_id' : note_id}, { '$addToSet' : {'fb_link' : new_fb_link}})
	return "Facebook link added !"

@app.route('/add_blog_link/<note_id>', methods=['POST'])
def add_blog_link(note_id):
	new_blog_link = request.form['blog']
	mongo.db.test.update({'_id' : note_id}, { '$addToSet' : {'blog_link' : new_blog_link}})
	return "Blog link added !"

@app.route('/add_insta_link/<note_id>', methods=['POST'])
def add_insta_link(note_id):
	new_insta_link = request.form['instagram']
	mongo.db.test.update({'_id' : note_id}, { '$addToSet' : {'insta_link' : new_insta_link}})
	return "Instagram link added !"

if __name__ == '__main__':
	app.run(debug=True)