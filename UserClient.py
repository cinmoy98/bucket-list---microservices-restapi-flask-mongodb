import requests

class UserClient:

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
			dt = response.json()
			if dt['access_token'] is not None:
				tokens = {
				'access_token' : dt['access_token'],
				'refresh_token' : dt['refresh_token']
				}
		return tokens

