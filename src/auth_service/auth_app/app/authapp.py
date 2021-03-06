from flask import  make_response, request, jsonify
from passlib.hash import sha256_crypt
from app.UserModel.UserModel import User, Auth
import datetime
from flask_pymongo import PyMongo
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt, 
	set_access_cookies, unset_jwt_cookies)
from flask_jwt_extended import JWTManager
from bson import ObjectId
import json

from app import uapp

uapp.config["MONGO_URI"] = "mongodb://localhost:27017/bucket_list"
uapp.config['SECRET_KEY'] = "Thisisreallysecret"
uapp.config['JWT_SECRET_KEY'] = "DoNotExpose"
#app.config['JWT_COOKIE_SECURE'] = False
#app.config['JWT_TOKEN_LOCATION'] = ["cookies"]
uapp.config['JWT_COOKIE_CSRF_PROTECT'] = False

#app.config['JWT_BLACKLIST_ENABLED'] = True
#app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
mongo = PyMongo(uapp)
jwt = JWTManager(uapp)



@uapp.route('/api/user/<string:username>/exists',methods=['GET'])
def get_username(username):
	user = User(mongo)
	response = user.get_username(username, mongo)
	print(response)
	if response['data'] is not None:
		return 'true', 200
	else:
		return 'false' , 404




@uapp.route('/api/user/create', methods=['POST'])
def post_register():
	user_data = {
	'username' : request.form['username'],
	'email' : request.form['email'],
	'first_name' : request.form['firstname'],
	'last_name' : request.form['lastname'],
	'password' : sha256_crypt.hash((str(request.form['password'])))
	}
	user = User(mongo)
	response = user.save_user(user_data, mongo)
	if response['data'] is not None:
		return "registerd",201
	else:
		return "registration-failed", 400




@uapp.route('/api/user/login', methods=["POST"])
def post_login():
	username = request.form['username']
	user = mongo.db.user.find_one({'username' : username})
	if user:
		if sha256_crypt.verify(str(request.form['password']), user['password']):
			access_expires = datetime.timedelta(minutes=4)
			refresh_expires = datetime.timedelta(minutes=60)
			access_token = create_access_token(identity = username , fresh = True, expires_delta=access_expires)
			refresh_token = create_refresh_token(identity = username, expires_delta = refresh_expires)
			tokens = {
			'msg': 'logged-in',
			'access_token': access_token,
			'refresh_token': refresh_token
			}
			return jsonify(tokens), 200
		else:
			return make_response(jsonify({'msg': 'wrong-password'})), 401
	return make_response(jsonify({'msg': 'user-not-found'})), 404




@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
	jti = jwt_payload["jti"]
	is_found = mongo.db.revoked_tokens.find_one({'jti':jti})
	return is_found is not None




@uapp.route('/api/user/logout',methods=['POST'])
@jwt_required()
def logout():
	jti = get_jwt()['jti']
	try:
		refresh_expires = datetime.timedelta(seconds=1)
		create_refresh_token(identity = "Expired", expires_delta = refresh_expires)
		revoked_token = Auth.add_revoked_token(jti, mongo)
		response = jsonify({"msg": "Logout Successful"})
		return response, 200
	except:
		return {'msg': 'something-went-wrong'}, 500



@uapp.route('/api/user/refresh', methods=['GET'])
@jwt_required(refresh=True)
def refresh():
	expires = datetime.timedelta(minutes=10)
	new_token = create_access_token(identity=get_jwt_identity(), fresh = False, expires_delta=expires)
	return jsonify(new_token)



@uapp.route('/protected',methods=['GET'])
@jwt_required()
def protected():
	return jsonify("protected")



@uapp.route('/test',methods=['GET'])
def test():
	user = mongo.db.user.find_one({'username' : 'cinmoy98'})
	print(user['password'])
	return "done"


