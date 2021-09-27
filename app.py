from flask import Flask
from flask import render_template, session, redirect, url_for, flash, request, jsonify, json, make_response
#from flask_login import current_user, LoginManager
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SelectField
import frontend_forms
from UserClient import UserClient
from BucketClient import BucketClient
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity ,get_jwt, set_access_cookies, set_refresh_cookies
import global_var
import pycountry
from functools import wraps
from flask_jwt_extended import decode_token
from datetime import datetime
from datetime import timedelta
from datetime import timezone
import requests


app = Flask(__name__)

bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = "Thisisreallysecret"
app.config['JWT_SECRET_KEY'] = "DoNotExpose"
app.config['WTF_CSRF_SECRET_KEY'] = "a csrf secret key"
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_COOKIE_CSRF_PROTECT'] = False

jwt = JWTManager(app)
global_var.init()


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
# 	return wrapper


@app.after_request
def refresh_expiring_jwts(response):
	try:
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
		return response


@app.route('/register', methods=['GET', 'POST'])
def register():
	form = frontend_forms.RegisterForm(request.form)
	if request.method == "POST":
		username = form.username.data
		user = UserClient.does_exist(username)
		if user:
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


@app.route('/login', methods=['GET', 'POST'])
def login():
	if UserClient.check_if_logged_in(request) == True:
		return render_template('dashboard.html', username = UserClient.get_user(request))
	else:
		form  = frontend_forms.LoginForm()
		if request.method == "POST":
			response,response_code = UserClient.post_login(form)
			if response_code==200:
				tokens = response.json()
				resp = make_response(render_template('dashboard.html', username = UserClient.get_user(tokens['access_token'])))
				set_access_cookies(resp, tokens['access_token'])
				set_refresh_cookies(resp, tokens['refresh_token'])
				return resp
			else:
				return render_template('login.html', form=form)
		return render_template('login.html', form=form)


@app.route('/check',methods=['GET'])
def check():
	# response = UserClient.check()
	# print("response checking in app")
	# print (response.status_code)
	# return response.json()
	return render_template('base.html', logged_in = False)

@app.route('/logout', methods=['POST', 'GET'])
def logout():
	response = UserClient.logout()
	if response:
		return response
	else:
		return "Something went wrong..."

@app.route('/create_note', methods=['GET', 'POST'])
def create_note():
	countries = list(pycountry.countries)
	form = frontend_forms.NewNote()
	categories = BucketClient.get_categories()
	form.category.choices = [(category, category) for category in categories]
	form.country.choices = [(country.name, country.name) for country in countries]
	if request.method == "POST":
		new_note = BucketClient.create_note(form)
	return render_template('new_nt.html', form = form)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
	form = frontend_forms.SelectForm()
	countries = BucketClient.get_countries()
	categories = BucketClient.get_categories()
	form.country.choices =[(country, country) for country in countries]
	form.country.choices.insert(0,('All','All'))
	form.city.choices.insert(0,('All','All'))
	buckets = BucketClient.get_notes()
	buckets = buckets.get_json()

    #categories = list(BucketClient.get)
	return render_template('bucket_board.html', form = form, buckets = buckets, categories=categories)

@app.route('/city/<country>')
def get_city(country):
	if country == 'None':
		city_not_selected=[]
		city_not_selected = [{'cityname':'Select Country', 'cityvalue':'All'}]
		return jsonify({'cities' : city_not_selected})
	cities = BucketClient.get_cities(country)
	cityArray = []

	for city in cities:
		cityobj = {}
		cityobj['cityname'] = city
		cityobj['cityvalue'] = city
		cityArray.append(cityobj)
	cityArray.insert(0, {'cityname':'Select City', 'cityvalue':'All'})
	return jsonify({'cities' : cityArray})

@app.route('/user_buckets', methods=['POST'])
def user_buckets():
	quer = request.json
	print(quer)
	bucket = BucketClient.get_notes_by_query(quer)
	bucket = bucket.get_json()
	#bucket = json.dumps(bucket)
	# buckets = {
	# "country":['cinmoy', 'gourob', 'ayon'],
	# "city":"Brahmanabria",
	# "uid":"cinmoy98"
	# }

	return jsonify(bucket)

@app.route('/buckets_by_category/<category>', methods=['POST'])
def buckets_by_category(category):
	print(category)
	response = BucketClient.get_by_category(category)
	return response



if __name__ == '__main__':
	app.run(debug=True)
