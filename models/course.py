from db import db
from superclass import Superclass

class CourseModel(Superclass):
	__tablename__ = 'studien'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	content = db.Column(db.String(200))
	
	fachbereich_id = db.Column(db.Integer, db.ForeignKey('faculties.id'))
	fachbereich = db.relationship('FacultyModel')


	def __init__(self, name, content, faculty_id):
		self.name = name
		self.content = content
		self.faculty_id = faculty_id

	def json(self):
		return { 'name': self.name, 'id': self.id, 'content': self.content }

	@classmethod
	def find_by_name(cls, name):
		return cls.query.filter_by(name=name).first()  # SELECT * FROM items WHERE name=name LIMIT 1