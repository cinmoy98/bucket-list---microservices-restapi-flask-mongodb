from flask import jsonify
import requests
from functools import wraps
from flask_jwt_extended import decode_token
from datetime import datetime
from datetime import timedelta
from datetime import timezone
import json

class BucketClient:

	def __init__(self):
		self.cookies = None


	def check_response_status_code(response):
		code = response.status_code
		res = response.json()['msg']
		print(res)
		if code == 401:
			if res == "Missing Authorization Header":
				return "You have to login first."
			elif res == "Token has expired":
				return "Session expired. Log in again."
			elif res == "Fresh token required":
				return "Give your credentials again to continue."
			else:
				return "Unknown error ! Try logging again."
		elif code == 422:
			if res == "Signature verification failed":
				return "Signature verification failed"
			else:
				return "Unknown error ! Try logging again."
		else:
			return "Unknown error ! Try logging again."


	# def verify_token():
	# 	def wrapper(fn):
	# 		@wraps(fn)
	# 		def decorator(*args,**kwargs):
	# 			decoded_token = decode_token(global_var.tokens['access_token'], allow_expired=True)
	# 			exp_timestamp = decoded_token['exp']
	# 			now = datetime.now(timezone.utc)
	# 			target_timestamp = datetime.timestamp(now + timedelta(minutes=5))
	# 			if target_timestamp > exp_timestamp:
	# 				url = 'http://127.0.0.1:5000/api/user/refresh'
	# 				headers = {'Authorization': 'Bearer '+global_var.tokens["refresh_token"]}
	# 				response = requests.request("GET", url = url, headers=headers)
	# 				if response.status_code == 200:
	# 					new_token = response.json()
	# 					global_var.tokens['access_token'] = new_token
	# 					return fn(*args, **kwargs)
	# 				else:
	# 					return(BucketClient.check_response_status_code(response))
	# 			else:
	# 				return fn(*args, **kwargs)
	# 		return decorator
	# 	return wrapper

	@staticmethod
	def get_notes(request):
		url = 'http://127.0.0.3:5000/api/bucket/allNotes'
		headers = {'Authorization': 'Bearer '+request.cookies['access_token_cookie']}
		response = requests.request("GET", url = url, headers=headers)
		if response:
			responsearray = json.loads(response.text)
			return jsonify(responsearray)


	@staticmethod
	def get_notes_by_query(quer, request):
		url = 'http://127.0.0.3:5000/api/bucket/notesByQuery'

		query ={}

		if quer[0] != 'All':
			query['category'] = quer[0]
		if quer[1] != 'All':
			query['country'] = quer[1]
		if quer[2] != 'All':
			query['city'] = quer[2]
		#print(query)
		headers = {'Authorization': 'Bearer '+request.cookies['access_token_cookie']}
		response = requests.request("GET", url = url, headers=headers, json = query)
		if response:
			responsearray = json.loads(response.text)
			return jsonify(responsearray)

	@staticmethod
	def get_by_category(category, request):
		url = 'http://127.0.0.3:5000/get_category/'+ category
		headers = {'Authorization': 'Bearer '+request.cookies['access_token_cookie']}
		response = requests.request("GET", url = url, headers=headers)
		print(response.json())
		if response:
			return jsonify(response.json())

	@staticmethod
	def get_countries(request):
		url = 'http://127.0.0.3:5000/api/bucket/distinctCountries'
		headers = {'Authorization': 'Bearer '+request.cookies['access_token_cookie']}
		response = requests.request("GET", url = url, headers=headers)
		#print(responsearray)
		if response:
			responsearray=json.loads(response.text)
			return responsearray

	@staticmethod
	def get_categories(request):
		url = 'http://127.0.0.3:5000/api/bucket/distictCat'
		headers = {'Authorization': 'Bearer '+request.cookies['access_token_cookie']}
		response = requests.request("GET", url = url, headers=headers)
		#print(responsearray)
		if response:
			responsearray=json.loads(response.text)
			return responsearray

	@staticmethod
	def get_cities(country,request):
		url = 'http://127.0.0.3:5000/api/bucket/cities/'+country
		headers = {'Authorization': 'Bearer '+request.cookies['access_token_cookie']}
		response = requests.request("GET", url = url, headers=headers)
		if response:
			responsearray=json.loads(response.text)
			return responsearray

	@staticmethod
	def create_note(form,request):
		payload = {
		'title' : form.title.data,
		'description' : form.description.data,
		'category' : form.category.data,
		'country' : form.country.data,
		'city' : form.city.data,
		'yt_link' : form.yt_link.data,
		'fb_link' : form.fb_link.data,
		'blog_link' : form.blog_link.data,
		'insta_link' : form.insta_link.data,
		'gmap' : form.gmap.data
		}
		print(payload)
		url = 'http://127.0.0.3:5000/api/bucket/newNote'
		headers = {'Authorization': 'Bearer '+request.cookies['access_token_cookie']}
		response = requests.request("POST", url = url, headers=headers, data = payload)
		if response:
			return jsonify("success")