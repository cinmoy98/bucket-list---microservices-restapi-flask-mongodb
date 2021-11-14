from flask import Flask, request, jsonify, json
from datetime
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt, 
	set_access_cookies, unset_jwt_cookies)
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config['SECRET_KEY'] = "Thisisreallysecret"
app.config['JWT_SECRET_KEY'] = "DoNotExpose"
app.config['JWT_TOKEN_LOCATION'] = ["cookies"]

jwt = JWTManager(app)


@app.route('/',methods=['GET'])
def home():
	return jsonify("home")


@app.route('/login', methods=['POST', 'GET'])
def login():
	username = 'cinmoy'
	expires = datetime.timedelta(minutes=1)
	access_token = create_access_token(identity = username , fresh = True, expires_delta=expires)
	refresh_token = create_refresh_token(identity = username)
	tokens = {
	'message': 'User was created',
	'access_token': access_token,
	'refresh_token': refresh_token
	}
	 return jsonify(tokens)



@app.route('/protected',methods=['GET'])
@jwt_required()
def protected():
	return jsonify("protected")


if __name__ == '__main__':
	app.run(host = '127.0.0.2', port=5000, debug=True)