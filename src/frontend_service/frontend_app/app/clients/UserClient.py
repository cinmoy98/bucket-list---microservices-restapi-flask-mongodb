import requests
# from flask import redirect,url_for
# from functools import wraps
from flask_jwt_extended import decode_token
from datetime import datetime
# from datetime import timedelta
from datetime import timezone
# import json

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

	@staticmethod
	def does_exist(username):
		url = 'http://127.0.0.2:5000/api/user/'+username+'/exists'
		response = requests.request("GET", url=url)
		return response.status_code == 200



	@staticmethod
	def post_user_create(form):
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
				# global_var.tokens = {
				# 'access_token' : dt['access_token'],
				# 'refresh_token' : dt['refresh_token']
				# }
				return response, response.status_code
			else:
				return "failed", 401

	def check_if_logged_in(request):
		if 'access_token_cookie' in request.cookies:
			decoded_token = decode_token(request.cookies['access_token_cookie'], allow_expired=True)
			exp_timestamp = decoded_token['exp']
			now = datetime.now(timezone.utc)
			now_timestamp = datetime.timestamp(now)
			if now_timestamp <= exp_timestamp:
				return True
			else:
				return False
		else:
			return False

	@staticmethod
	def get_user(access_token):
		decoded_token = decode_token(access_token, allow_expired=True)
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