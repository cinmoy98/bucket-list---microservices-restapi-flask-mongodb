import requests
from functools import wraps
from flask_jwt_extended import decode_token
from datetime import datetime
from datetime import timedelta
from datetime import timezone
class UserClient:

	def __init__(self):
		self.cookies = None

	
	def verify_token():
		def wrapper(fn):
			@wraps(fn)
			def decorator(*args,**kwargs):
				decoded_token = decode_token(tokens['access_token'], allow_expired=True)
				exp_timestamp = decoded_token['exp']
				now = datetime.now(timezone.utc)
				target_timestamp = datetime.timestamp(now + timedelta(minutes=5))
				if target_timestamp > exp_timestamp:
					url = 'http://127.0.0.1:5000/api/user/refresh'
					headers = {'Authorization': 'Bearer '+tokens["refresh_token"]}
					response = requests.request("GET", url = url, headers=headers)
					if response:
						new_token = response.json()
						tokens['access_token'] = new_token
						return fn(*args, **kwargs)
				else:
					return fn(*args, **kwargs)
			return decorator
		return wrapper


	@staticmethod
	def does_exist(username):
		url = 'http://127.0.0.1:5000/api/user/'+username+'/exists'
		response = requests.request("GET", url=url)
		return response.status_code == 200


	@staticmethod
	def post_user_create(form):
		user = False
		payload = {
		'username' : form.username.data,
		'email' : form.email.data,
		'firstname' : form.first_name.data,
		'lastname' : form.last_name.data,
		'password' : form.password.data
		}
		print(payload)
		url = 'http://127.0.0.1:5000/api/user/create'
		response = requests.request("POST", url = url, data=payload)
		if response:
			user = 'CREATED'
		return user


	@staticmethod
	def post_login(form):
		global tokens
		tokens = {
		'access_token' : None ,
		'refresh_token' : None
		}
		payload = {
		'username' : form.username.data,
		'password' : form.password.data
		}

		url = 'http://127.0.0.1:5000/api/user/login'
		response = requests.request("POST", url=url, data=payload)
		if response:
			#UserClient.cookies = response.cookies
			dt = response.json()
			if dt['access_token'] is not None:
				tokens = {
				'access_token' : dt['access_token'],
				'refresh_token' : dt['refresh_token']
				}
			return "Login Successful"

	@staticmethod
	@verify_token()
	def check():
		url = 'http://127.0.0.1:5000/protected'
		#print(UserClient.cookies)
		headers = {'Authorization': 'Bearer '+tokens["access_token"]}
		response = requests.request("GET", url = url, headers=headers)
		#print (response.json())
		if response:
			return response.json()

	@staticmethod
	def logout():
		url = "http://127.0.0.1:5000/api/user/logout"
		headers = {'Authorization': 'Bearer '+tokens["access_token"]}
		response = requests.request("POST", url = url, headers=headers)
		if response:
			dt = response.json()
			if dt['msg'] == "logout successful":
				tokens['access_token'] = None
				tokens['refresh_token'] = None
			return "Logout Successful"


	# @staticmethod
	# def refresh():
	# 	url = 'http://127.0.0.2:5000/api/user/refresh'
	# 	headers = {'Authorization': 'Bearer '+tokens["refresh_token"]}
	# 	response = requests.request("GET", url = url, headers=headers)
	# 	if response:
	# 		print(response.json())
	# 		return "Refresh done"