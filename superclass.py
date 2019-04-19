class Superclass(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	# created at, updated at etc.
	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()

	def json(self):
		raise NotImplementedError()  # raise error if json has not been defined in a subclass