from flask import Flask
from flask import render_template, session, redirect, url_for, flash, request
from flask_login import current_user, LoginManager
from flask_bootstrap import Bootstrap
import frontend_forms
from UserClient import UserClient


app = Flask(__name__)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'main.login'

bootstrap = Bootstrap(app)

app.config.update(dict(
	SECRET_KEY="powerful secretkey",
	WTF_CSRF_SECRET_KEY="a csrf secret key",
	))


# @app.route('/register', methods=['GET', 'POST'])
# def register():
# 	form = frontend_forms.RegisterForm(request.form)
# 	if request.method == "POST":
# 		if form.validate_on_submit():
# 			username = form.username.data
# 			user = UserClient.does_exist(username)

@app.route('/check/<string:username>',methods=['GET'])
def check(username):
	user = UserClient.does_exist(username)
	if user:
		return "found"
	else:
		return "Not found"


if __name__ == '__main__':
	app.run(host = '127.0.0.2', port=5000, debug=True)