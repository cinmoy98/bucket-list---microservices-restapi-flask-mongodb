import uuid
import datetime
from bson.objectid import ObjectId

class Note(object):
	def __init__(self,uid ,req , _id = None):
		self.uid = uid
		self.title = req['title']
		self.description = req['description']
		self.category = req.getlist('category')
		self.country = req['country']
		self.city = req['city']
		self.yt_link = req.getlist('yt_link')
		self.fb_link = req.getlist('fb_link')
		self.blog_link = req.getlist('blog_link')
		self.insta_link = req.getlist('insta_link')
		self.gmap = req['gmap']
		self._id = uuid.uuid4().hex if _id is None else _id
	

	def save_it(self, mongo):
		mongo.db.buckets.insert(self.json(up=False))

	def update_it(self,note_id, mongo):
		mongo.db.test.update({'_id' : note_id}, {"$set": self.json(up=True)})


	def json(self, up):
		json_ob =  {
			'uid' : self.uid,
			'description' : self.description,
			'category' : self.category,
			'country' : self.country,
			'city' : self.city,
			'yt_link' : self.yt_link,
			'fb_link' : self.fb_link,
			'blog_link' : self.blog_link,
			'insta_link' : self.insta_link,
			'gmap' : self.gmap
		}
		if up == False:
			json_ob['_id'] = self._id
		
		return json_ob

	@staticmethod
	def get_output(notes):
		extract_output = [{
				'uid' : user['uid'],
				'description' : user['description'],
				'category' : user['category'],
				'country': user['country'],
				'city' : user['city'],
				'yt_link' : user['yt_link'],
				'fb_link' : user['fb_link'],
				'blog_link' : user['blog_link'],
				'insta_link' : user['insta_link'],
				'gmap' : user['gmap']
				} for user in notes]
		return extract_output

	@staticmethod
	def find_all_notes(mongo, username):
		notes = mongo.db.buckets.find({'uid':username})
		return(Note.get_output(notes))

	@staticmethod
	def find_by_query(mongo, query):
		notes = mongo.db.buckets.find(query)
		return(Note.get_output(notes))


	@staticmethod
	def find_by_note_id(id, mongo):
		note = mongo.db.test.find_one({'_id': id})
		#return(Note.get_output(note))
		return note

	@staticmethod
	def delete_note_by_id(note_id, mongo):
		mongo.db.test.delete_one({'_id' : note_id})

	@staticmethod
	def find_by_city(city, mongo):
		notes = mongo.db.test.find({'city' : city})
		return (Note.get_output(notes))
		

	@staticmethod
	def find_by_country(country, mongo):
		notes = mongo.db.test.find({'country' : country})
		return (Note.get_output(notes))

	@staticmethod
	def find_by_category(category, mongo, username):
		notes = mongo.db.buckets.find({'category' : category, 'uid' : username})
		return (Note.get_output(notes))

