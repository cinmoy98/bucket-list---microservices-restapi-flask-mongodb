from flask import Flask
from flask import render_template, session, redirect, url_for, flash, request, jsonify, json
#from flask_login import current_user, LoginManager
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SelectField
import frontend_forms
from UserClient import UserClient
from BucketClient import BucketClient
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity ,get_jwt
import global_var
import pycountry


app = Flask(__name__)

#login_manager = LoginManager(app)
#login_manager.init_app(app)
#login_manager.login_view = 'main.login'

bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = "Thisisreallysecret"
app.config['JWT_SECRET_KEY'] = "DoNotExpose"
app.config['WTF_CSRF_SECRET_KEY'] = "a csrf secret key"

jwt = JWTManager(app)
global_var.init()


@app.route('/register', methods=['GET', 'POST'])
def register():
	form = frontend_forms.RegisterForm(request.form)
	if request.method == "POST":
		username = form.username.data
		user = UserClient.does_exist(username)
		if user:
			flash('Please try another username', 'error')
			return render_template('signup.html', form=form)
		else:
			user = UserClient.post_user_create(form)
			if user:
				flash('Thanks for registering, please login to continue', 'success')
				return redirect(url_for('login'))
	else:
		flash('Errors found', 'error')
	return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
	if UserClient.check_if_logged_in() == True:
		print('inside already logged in')
		return render_template('dashboard.html', username = UserClient.get_user())
	else:
		print(UserClient.check_if_logged_in())
		form  = frontend_forms.LoginForm()
		if request.method == "POST":
			msg = UserClient.post_login(form)
			if msg == "Login Successful":
				# username = UserClient.get_user()
				print('inside logged in')
				return render_template('dashboard.html', username = UserClient.get_user())
				#return global_var.tokens
	                # if form.username.data == "cinmoy98":
	                #         return render_template('home.html', username = form.username.data)
			# print(access_token)
			# username = get_jwt_identity(access_token['access_token'])
		return render_template('login.html', form=form)


@app.route('/check',methods=['GET'])
def check():
	response = UserClient.check()
	#print (response)
	return render_template('home.html', response = response)

@app.route('/logout', methods=['POST', 'GET'])
def logout():
	response = UserClient.logout()
	return response

@app.route('/create_note', methods=['GET', 'POST'])
def create_note():
	countries = list(pycountry.countries)
	form = frontend_forms.NewNote()
	categories = BucketClient.get_categories()
	form.category.choices = [(category, category) for category in categories]
	form.country.choices = [(country.name, country.name) for country in countries]
	if request.method == "POST":
		new_note = BucketClient.create_note(form)
	return render_template('new_note.html', form = form)

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
	bucket = BucketClient.get_notes_by_query(quer)
	bucket = bucket.get_json()
	#bucket = json.dumps(bucket)
	print(bucket[0])

	buckets = {
	"country":['cinmoy', 'gourob', 'ayon'],
	"city":"Brahmanabria",
	"uid":"cinmoy98"
	}

	return jsonify(bucket)

@app.route('/buckets_by_category/<category>', methods=['POST'])
def buckets_by_category(category):
	print(category)
	response = BucketClient.get_by_category(category)
	return response



if __name__ == '__main__':
	app.run(host = '127.0.0.2', port=5000, debug=True)
