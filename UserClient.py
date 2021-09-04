import requests
from flask import redirect,url_for
from functools import wraps
from flask_jwt_extended import decode_token
from datetime import datetime
from datetime import timedelta
from datetime import timezone
import global_var
import json

class UserClient:

	def __init__(self):
		self.cookies = None


	def check_response_status_code(response):
		code = response.status_code
		res = response.json()['msg']
		if code == 401:
			if res == "Missing Authorization Header":
				return "You have to login first."
			elif res == "Token has expired":
				return "Session expired. Log in again."
			elif res == "Fresh token required":
				return "Give your credentials again to continue."
			elif res == "Token has been revoked":
				return "Session expired. Log in again."
			else:
				return "Unknown error ! Try logging again."
		elif code == 422:
			if res == "Signature verification failed":
				return "Signature verification failed"
			else:
				return "Unknown error ! Try logging again."
		else:
			return "Unknown error ! Try logging again."


	def verify_token():
		def wrapper(fn):
			@wraps(fn)
			def decorator(*args,**kwargs):
				if global_var.tokens['access_token'] == None:
					redirect(url_for('login'))
				decoded_token = decode_token(global_var.tokens['access_token'], allow_expired=True)
				exp_timestamp = decoded_token['exp']
				now = datetime.now(timezone.utc)
				target_timestamp = datetime.timestamp(now + timedelta(minutes=5))
				if target_timestamp > exp_timestamp:
					url = 'http://127.0.0.2:5000/api/user/refresh'
					headers = {'Authorization': 'Bearer '+global_var.tokens["refresh_token"]}
					response = requests.request("GET", url = url, headers=headers)
					
					if response.status_code == 200:
						new_token = response.json()
						global_var.tokens['access_token'] = new_token
						print("refreshed")
						return fn(*args, **kwargs)
					else:
						return(UserClient.check_response_status_code(response))
				else:
					return fn(*args, **kwargs)
			return decorator
		return wrapper


	@staticmethod
	def does_exist(username):
		url = 'http://127.0.0.2:5000/api/user/'+username+'/exists'
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
		url = 'http://127.0.0.2:5000/api/user/create'
		response = requests.request("POST", url = url, data=payload)
		if response:
			return response


	@staticmethod
	def post_login(form):
		payload = {
		'username' : form.username.data,
		'password' : form.password.data
		}

		url = 'http://127.0.0.2:5000/api/user/login'
		response = requests.request("POST", url=url, data=payload)
		if response:
			#UserClient.cookies = response.cookies
			dt = response.json()
			if dt['access_token'] is not None:
				global_var.tokens = {
				'access_token' : dt['access_token'],
				'refresh_token' : dt['refresh_token']
				}
			return response.status_code

	def check_if_logged_in():
		if global_var.tokens['access_token'] == None:
			return False
		else:
			return True

	@staticmethod
	def get_user():
		decoded_token = decode_token(global_var.tokens['access_token'], allow_expired=True)
		return decoded_token['sub']


	@staticmethod
	def check():
		url = 'http://127.0.0.2:5000/protected'
		headers = {'Authorization': 'Bearer '+global_var.tokens["access_token"]}
		response = requests.request("GET", url = url, headers=headers)
		if response.status_code == 200:
			return response
		else:
			print(response.json())
			return response
			#return(UserClient.check_response_status_code(response))

	@staticmethod
	def logout():
		url = "http://127.0.0.2:5000/api/user/logout"
		headers = {'Authorization': 'Bearer '+global_var.tokens["access_token"]}
		response = requests.request("POST", url = url, headers=headers)
		if response:
			if response.status_code == 200:
				global_var.tokens['access_token'] = None
				global_var.tokens['refresh_token'] = None
				return response.text
			else:
				return(UserClient.check_response_status_code(response))