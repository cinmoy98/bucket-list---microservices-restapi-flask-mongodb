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

@app.route('/login', methods=['POST', 'GET'])
def login():
	url = 'http://127.0.0.2:5000/login'
	response = requests.request("POST", url=url)
	if response:
		data = response.json()
		tokens = {
		'access_token' : dt['access_token'],
		'refresh_token' : dt['refresh_token']
		}
	print(tokens)


if __name__ == '__main__':
	app.run(debug=True)