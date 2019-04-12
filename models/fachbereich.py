from db import db


class FachbereichModel(db.Model):
	__tablename__ = 'fachbereiche'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))

	uni_id = db.Column(db.Integer, db.ForeignKey('unis.id'))
	uni = db.relationship('UniModel')
	studien = db.relationship('StudiumModel', lazy='dynamic') 

	def __init__(self, name, uni_id):
		self.name = name
		self.uni_id = uni_id

	def json(self):
		return { 'name': self.name, 'id': self.id, 'studien': [studium.json() for studium in self.studien.all()]}

	@classmethod
	def find_by_name(cls, name):
		return cls.query.filter_by(name=name).first()  # SELECT * FROM items WHERE name=name LIMIT 1

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()