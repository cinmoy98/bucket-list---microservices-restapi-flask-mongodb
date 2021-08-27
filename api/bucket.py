from flask import Flask, jsonify, request, redirect, render_template 
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import json
from bson import BSON
from bson import json_util
import shortuuid
from models.notes import Note
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager

app = Flask(__name__)
# MONGO URI is used for connecting the app to the mongodb atlas.Copy the connection string from atlas.
# app.config["MONGO_URI"] = "mongodb+srv://m001-student:m001-mongodb-basics@sandbox.ewm7q.mongodb.net/bucket_list?retryWrites=true&w=majority"
app.config["MONGO_URI"] = "mongodb://localhost:27017/bucket_list"
# app.config['SECRET_KEY'] = "Thisisreallysecret"
# app.config['JWT_SECRET_KEY'] = "DoNotExpose"
# app.config['JWT_TOKEN_LOCATION'] = ['headers', 'query_string']
# app.config['JWT_HEADER_NAME'] = ["Authorization"]
# app.config['JWT_HEADER_TYPE'] = ["Bearer"]

app.config['SECRET_KEY'] = "Thisisreallysecret"
app.config['JWT_SECRET_KEY'] = "DoNotExpose"

mongo = PyMongo(app)
jwt = JWTManager(app)


@app.route('/create_note',methods=['POST'])
@jwt_required()
def create_note_test():
	if request.method == 'POST':
		uid = get_jwt_identity()
		req = request.form
		new_note = Note(uid, req)
		new_note.save_it(mongo)
	return "created",201




@app.route('/getnotes',methods=['GET'])
@jwt_required()
def get_notes():
	auth_header = request.headers.get('Authorization', None)
	username = get_jwt_identity()
	notes = Note.find_all_notes(mongo, username)
	return jsonify(notes)

@app.route('/get_notes_by_query', methods=['GET'])
@jwt_required()
def get_notes_by_query():
	uid = get_jwt_identity()
	query = request.json
	query['uid'] = uid
	notes = Note.find_by_query(mongo, query)
	return jsonify(notes)

# getnote recieves _id of a particular note and fetch that note.
@app.route('/getnote/<string:note_id>',methods=['GET'])
def get_note(note_id):
	note = Note.find_by_note_id(note_id, mongo)
	print(note['title'])
	return jsonify(note)



@app.route('/get_categories', methods=['GET'])
@jwt_required()
def get_categories():
	uid = get_jwt_identity()
	db_ops = mongo.db.buckets
	categories = db_ops.distinct("category", {"uid" : uid})
	return jsonify(categories)

# @app.route('/get_category/<catg>',methods=['GET'])
# @jwt_required()
# def get_category(catg):
# 	username = get_jwt_identity()
# 	notes = Note.find_by_category(catg, mongo, username)
# 	print(jsonify(notes))
# 	return jsonify(notes)


# @app.route('/get_country/<string:country>', methods=['GET'])
# def get_country(country):
# 	notes = Note.find_by_country(country, mongo)
# 	return jsonify(notes)



# @app.route('/get_city/<string:city>', methods=['GET'])
# def get_city(city):
# 	notes = Note.find_by_city(city, mongo)
# 	return jsonify(notes)



@app.route('/get_cities/<string:country>', methods=['GET'])
@jwt_required()
def get_cities(country):
	uid = get_jwt_identity()
	db_ops = mongo.db.buckets

	cities = db_ops.distinct("city", {"country" : country, "uid" : uid})
	#output = [{city['city']} for city in cities]
	return jsonify(cities)


@app.route('/get_countries',methods=['GET'])
@jwt_required()
def get_countries():
	uid = get_jwt_identity()
	db_ops = mongo.db.buckets

	countries = db_ops.distinct("country", {"uid" : uid})
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
	app.run(host = '127.0.0.3', port=5000, debug=True)
