from flask import Flask, make_response, request, jsonify, json
from passlib.hash import sha256_crypt
from UserModel import User, Auth
import datetime
from flask_pymongo import PyMongo
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt, 
	set_access_cookies, unset_jwt_cookies)
from flask_jwt_extended import JWTManager
from bson import ObjectId

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/bucket_list"
app.config['SECRET_KEY'] = "Thisisreallysecret"
app.config['JWT_SECRET_KEY'] = "DoNotExpose"
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_TOKEN_LOCATION'] = ["cookies"]

#app.config['JWT_BLACKLIST_ENABLED'] = True
#app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
mongo = PyMongo(app)
jwt = JWTManager(app)


@app.route('/api/user/<string:username>/exists',methods=['GET'])
def get_username(username):
	user = User(mongo)
	response = user.get_username(username, mongo)
	print(response)
	if response['data'] is not None:
		return 'true'
	else:
		return 'false' , 404


@app.route('/api/user/create', methods=['POST'])
def post_register():
	user_data = {
	'username' : request.form['username'],
	'email' : request.form['email'],
	'first_name' : request.form['firstname'],
	'last_name' : request.form['lastname'],
	'password' : sha256_crypt.hash((str(request.form['password'])))
	}
	print(user_data)
	user = User(mongo)
	response = user.save_user(user_data, mongo)
	if response['data'] is not None:
		return "registerd !"
	else:
		return "Not registered !"


@app.route('/api/user/login', methods=["POST"])
def post_login():
	giver_password = None
	username = request.form['username']
	user = mongo.db.user.find_one({'username' : username})
	if user:
		if sha256_crypt.verify(str(request.form['password']), user['password']):
			expires = datetime.timedelta(minutes=10)
			access_token = create_access_token(identity = username , fresh = True, expires_delta=expires)
			refresh_token = create_refresh_token(identity = username)
			# tokens = {
			# 'message': 'User was created',
			# 'access_token': access_token,
			# 'refresh_token': refresh_token
			# }
			#return jsonify(tokens)
			response = jsonify({'message': 'success'})
			set_access_cookies(response, access_token)
			return response
		else:
			return make_response(jsonify({'message': 'Wrong Password !'}))
	return make_response(jsonify({'message': 'User Not Found'})), 401


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
	jti = jwt_payload["jti"]
	is_found = mongo.db.revoked_tokens.find_one({'jti':jti})
	return is_found is not None

@app.route('/api/user/logout',methods=['POST'])
@jwt_required()
def logout():
	jti = get_jwt()['jti']
	try:
		revoked_token = Auth.add_revoked_token(jti, mongo)
		res = {'message': 'Access token revoked'}
		unset_jwt_cookies(res)
		return res
	except:
		return {'message': 'Something went wrong'}, 500



@app.route('/protected',methods=['GET'])
@jwt_required()
def protected():
	return "protected"


@app.route('/test',methods=['GET'])
def test():
	user = mongo.db.user.find_one({'username' : 'cinmoy98'})
	print(user['password'])
	return "done"

if __name__ == '__main__':
	app.run(debug=True)