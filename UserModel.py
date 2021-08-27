import datetime
from werkzeug.security import check_password_hash
from flask_pymongo import PyMongo


class User:

	def __init__(self, user_collection):
		self.collection = user_collection
		self.username = None
		self.email = None
		self.response = {'error': None, 'data': None}


	@staticmethod
	def validate_login(password_hash, password):
		return check_password_hash(password_hash, password)


	def get_username(self, user_name, mongo):
		self.response['error'] = None
		try:
			user = mongo.db.user.find_one({'username' : user_name})
			self.response['data'] = user

		except:
			self.response['error'] = 'User Not Found'

		return self.response


	def save_user(self,user_data, mongo):
		self.response['error'] = None
		try:
			user = mongo.db.user.insert(user_data)
			self.response['data'] = user_data

		except:
			self.response['error'] = 'Registration failed'

		return self.response

class Auth:

	@staticmethod
	def add_revoked_token(jti, mongo):
		mongo.db.revoked_tokens.insert({'jti' : jti})

	# @staticmethod
	# def is_jti_blacklisted(jti, mongo):
	# 	is_found = mongo.db.revoked_tokens.find({'jti':jti})
	# 	return bool(is_found)

