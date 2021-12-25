from flask import Flask
from flask import render_template, session, redirect, url_for, flash, request, jsonify, json, make_response
#from flask_login import current_user, LoginManager
#from flask_bootstrap import Bootstrap
# from flask_wtf import FlaskForm
# from wtforms import SelectField
from app import frontend_forms
from app.clients.UserClient import UserClient
from app.clients.BucketClient import BucketClient
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity ,get_jwt, set_access_cookies, set_refresh_cookies, unset_jwt_cookies
import pycountry
from functools import wraps
from flask_jwt_extended import decode_token
from datetime import datetime
from datetime import timedelta
from datetime import timezone
import requests
from app import fapp

#bootstrap = Bootstrap(fapp)

fapp.config['SECRET_KEY'] = "Thisisreallysecret"
fapp.config['JWT_SECRET_KEY'] = "DoNotExpose"
fapp.config['WTF_CSRF_SECRET_KEY'] = "a csrf secret key"
fapp.config['JWT_TOKEN_LOCATION'] = ['cookies']
fapp.config['JWT_COOKIE_SECURE'] = False
fapp.config['JWT_COOKIE_CSRF_PROTECT'] = False

jwt = JWTManager(fapp)

# def verify_token():
# 	def wrapper(fn):
# 		@wraps(fn)
# 		def decorator(*args,**kwargs):
# 			if request.cookies['access_token_cookie'] == None:
# 				return redirect(url_for('login'))
# 			decoded_token = decode_token(request.cookies['access_token_cookie'], allow_expired=True)
# 			exp_timestamp = decoded_token['exp']
# 			now = datetime.now(timezone.utc)
# 			if datetime.timestamp(now) > exp_timestamp:
# 				global_var.init()
# 				return redirect(url_for('login'))
# 			target_timestamp = datetime.timestamp(now + timedelta(minutes=5))
# 			if target_timestamp > exp_timestamp:
# 				url = 'http://127.0.0.2:5000/api/user/refresh'
# 				headers = {'Authorization': 'Bearer '+request.cookies['refresh_token_cookie']}
# 				response = requests.request("GET", url = url, headers=headers)
				
# 				if response.status_code == 200:
# 					new_token = response.json()
# 					global_var.tokens['access_token'] = new_token
# 					return fn(*args, **kwargs)
# 				# else:
# 				# 	return(UserClient.check_response_status_code(response))
# 			else:
# 				return fn(*args, **kwargs)
# 		return decorator
# 	return wrfapper


@fapp.after_request
def refresh_expiring_jwts(response):
	try:
		print(request.cookies['access_token_cookie'])
		decoded_token = decode_token(request.cookies['access_token_cookie'], allow_expired=True)
		exp_timestamp = decoded_token['exp']
		now = datetime.now(timezone.utc)
		target_timestamp = datetime.timestamp(now + timedelta(minutes=5))
		if target_timestamp > exp_timestamp:
			url = 'http://127.0.0.2:5000/api/user/refresh'
			headers = {'Authorization': 'Bearer '+request.cookies['refresh_token_cookie']}
			print(headers)
			resp = requests.request("GET", url = url, headers=headers)
			if resp:
				new_token = resp.json()
				set_access_cookies(response, new_token)
				print("token refreshed")
		return response
	except:
		print("Except executed")
		return response


@fapp.route('/register', methods=['GET', 'POST'])
def register():
	form = frontend_forms.RegisterForm(request.form)
	if request.method == "POST":
		username = form.username.data
		user = UserClient.does_exist(username)
		if user.status_code==200:
			#flash('Please try another username', 'error')
			return render_template('signup.html', form=form)
		else:
			user = UserClient.post_user_create(form)
			if user.status_code==200:
				#flash('Thanks for registering, please login to continue', 'success')
				return redirect(url_for('login'))
			else:
				return render_template('signup.html', form=form)
	else:
		#flash('Errors found', 'error')
		return render_template('signup.html', form=form)
	return render_template('signup.html', form=form)


@fapp.route('/login', methods=['GET', 'POST'])
def login():
	if UserClient.check_if_logged_in(request) == True:
		return render_template('dashboard.html', username = UserClient.get_user(request, None))
	else:
		form  = frontend_forms.LoginForm()
		if request.method == "POST":
			response,response_code = UserClient.post_login(form)
			if response_code==200:
				tokens = response.json()
				print(tokens)
				resp = make_response(render_template('dashboard.html', username = UserClient.get_user(None,tokens['access_token'])))
				set_access_cookies(resp, tokens['access_token'])
				set_refresh_cookies(resp, tokens['refresh_token'])
				return resp
			else:
				return render_template('login.html', form=form)
		return render_template('login.html', form=form)


@fapp.route('/check',methods=['GET'])
def check():
	# response = UserClient.check()
	# print("response checking in fapp")
	# print (response.status_code)
	# return response.json()
	return render_template('bucket.html')

@fapp.route('/logout', methods=['POST', 'GET'])
def logout():
	response = UserClient.logout(request)
	if response:
		response = make_response(jsonify(response))
		unset_jwt_cookies(response, domain=None)
		return response
	else:
		return "Something went wrong..."

@fapp.route('/create_note', methods=['GET', 'POST'])
def create_note():
	countries = list(pycountry.countries)
	form = frontend_forms.NewNote()
	categories = BucketClient.get_categories(request)
	form.category.choices = [(category, category) for category in categories]
	form.country.choices = [(country.name, country.name) for country in countries]
	if request.method == "POST":
		new_note = BucketClient.create_note(form)
	return render_template('new_nt.html', form = form)

@fapp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
	form = frontend_forms.SelectForm()
	countries = BucketClient.get_countries(request)
	categories = BucketClient.get_categories(request)
	form.country.choices =[(country, country) for country in countries]
	form.country.choices.insert(0,('All','All'))
	form.city.choices.insert(0,('All','All'))
	buckets = BucketClient.get_notes(request)
	buckets = buckets.get_json()

    #categories = list(BucketClient.get)
	return render_template('bucket.html', form = form, buckets = buckets, categories=categories)

@fapp.route('/city/<country>')
def get_city(country):
	if country == 'None':
		city_not_selected=[]
		city_not_selected = [{'cityname':'Select Country', 'cityvalue':'All'}]
		return jsonify({'cities' : city_not_selected})
	cities = BucketClient.get_cities(country,request)
	cityArray = []

	for city in cities:
		cityobj = {}
		cityobj['cityname'] = city
		cityobj['cityvalue'] = city
		cityArray.append(cityobj)
	cityArray.insert(0, {'cityname':'Select City', 'cityvalue':'All'})
	return jsonify({'cities' : cityArray})

@fapp.route('/user_buckets', methods=['POST'])
def user_buckets():
	quer = request.json
	print(quer)
	bucket = BucketClient.get_notes_by_query(quer, request)
	bucket = bucket.get_json()
	#bucket = json.dumps(bucket)
	# buckets = {
	# "country":['cinmoy', 'gourob', 'ayon'],
	# "city":"Brahmanabria",
	# "uid":"cinmoy98"
	# }

	return jsonify(bucket)

@fapp.route('/buckets_by_category/<category>', methods=['POST'])
def buckets_by_category(category):
	print(category)
	response = BucketClient.get_by_category(category)
	return response




