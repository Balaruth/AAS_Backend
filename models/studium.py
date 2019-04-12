from db import db


class StudiumModel(db.Model):
	__tablename__ = 'studien'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	inhalt = db.Column(db.String(200))
	
	fachbereich_id = db.Column(db.Integer, db.ForeignKey('fachbereiche.id'))
	fachbereich = db.relationship('FachbereichModel')


	def __init__(self, name, inhalt, fachbereich_id):
		self.name = name
		self.inhalt = inhalt
		self.fachbereich_id = fachbereich_id

	def json(self):
		return { 'name': self.name, 'id': self.id, 'inhalt': self.inhalt }

	@classmethod
	def find_by_name(cls, name):
		return cls.query.filter_by(name=name).first()  # SELECT * FROM items WHERE name=name LIMIT 1

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()