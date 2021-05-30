from flask import Flask
from flask import render_template, session, redirect, url_for, flash, request
from flask_login import current_user, LoginManager
from flask_bootstrap import Bootstrap
import frontend_forms
from UserClient import UserClient
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity ,get_jwt


app = Flask(__name__)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'main.login'

bootstrap = Bootstrap(app)
jwt = JWTManager(app)

app.config.update(dict(
	SECRET_KEY="powerful secretkey",
	WTF_CSRF_SECRET_KEY="a csrf secret key",
	))


@app.route('/register', methods=['GET', 'POST'])
def register():
	form = frontend_forms.RegisterForm(request.form)
	if request.method == "POST":
		username = form.username.data
		user = UserClient.does_exist(username)
		if user:
			flash('Please try another username', 'error')
			return ' user exist ! register page, form=form'
		else:
			user = UserClient.post_user_create(form)
			if user:
				flash('Thanks for registering, please login to continue', 'success')
				return 'redirect, url for, frontend.login'
	else:
		flash('Errors found', 'error')


@app.route('/login', methods=['GET', 'POST'])
def login():
	form  = frontend_forms.LoginForm()
	if request.method == "POST":
		access_token = UserClient.post_login(form)
		# print(access_token)
		# username = get_jwt_identity(access_token['access_token'])
		return "done"



@app.route('/check',methods=['GET'])
def check():
	response = UserClient.check()
	print (response)
	return response

@app.route('/logout', methods=['POST'])
def logout():
	response = UserClient.logout()
	return response


if __name__ == '__main__':
	app.run(host = '127.0.0.2', port=5000, debug=True)