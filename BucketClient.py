import requests
import global_var
from flask import jsonify
import json

class BucketClient:

	def __init__(self):
		self.cookies = None


	@staticmethod
	def get_notes():
		url = 'http://127.0.0.3:5000/getnotes'
		headers = {'Authorization': 'Bearer '+global_var.tokens["access_token"]}
		response = requests.request("GET", url = url, headers=headers)
		if response:
			responsearray = json.loads(response.text)
			responsearray
			return jsonify(responsearray)


	@staticmethod
	def get_notes_by_query(quer):
		url = 'http://127.0.0.3:5000/get_notes_by_query'

		query ={}

		if quer[0] != 'All':
			query['category'] = quer[0]
		if quer[1] != 'All':
			query['country'] = quer[1]
		if quer[2] != 'All':
			query['city'] = quer[2]
		print(query)
		headers = {'Authorization': 'Bearer '+global_var.tokens["access_token"]}
		response = requests.request("GET", url = url, headers=headers, json = query)
		if response:
			responsearray = json.loads(response.text)
			return jsonify(responsearray)

	@staticmethod
	def get_by_category(category):
		url = 'http://127.0.0.3:5000/get_category/'+ category
		headers = {'Authorization': 'Bearer '+global_var.tokens["access_token"]}
		response = requests.request("GET", url = url, headers=headers)
		print(response.json())
		if response:
			return jsonify(response.json())

	@staticmethod
	def get_countries():
		url = 'http://127.0.0.3:5000/get_countries'
		headers = {'Authorization': 'Bearer '+global_var.tokens["access_token"]}
		response = requests.request("GET", url = url, headers=headers)
		#print(responsearray)
		if response:
			responsearray=json.loads(response.text)
			return responsearray

	@staticmethod
	def get_categories():
		url = 'http://127.0.0.3:5000/get_categories'
		headers = {'Authorization': 'Bearer '+global_var.tokens["access_token"]}
		response = requests.request("GET", url = url, headers=headers)
		#print(responsearray)
		if response:
			responsearray=json.loads(response.text)
			return responsearray

	@staticmethod
	def get_cities(country):
		url = 'http://127.0.0.3:5000/get_cities/'+country
		headers = {'Authorization': 'Bearer '+global_var.tokens["access_token"]}
		response = requests.request("GET", url = url, headers=headers)
		if response:
			responsearray=json.loads(response.text)
			return responsearray

	@staticmethod
	def create_note(form):
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
		url = 'http://127.0.0.3:5000/create_note'
		headers = {'Authorization': 'Bearer '+global_var.tokens["access_token"]}
		response = requests.request("POST", url = url, headers=headers, data = payload)
		if response:
			return jsonify("success")