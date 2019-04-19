from superclass import Superclass

class FacultyModel(Superclass):
	__tablename__ = 'faculties'

	
	name = db.Column(db.String(80))

	uni_id = db.Column(db.Integer, db.ForeignKey('unis.id'))
	uni = db.relationship('UniModel')
	courses = db.relationship('CourseModle', lazy='dynamic') 

	def __init__(self, name, uni_id):
		self.name = name
		self.uni_id = uni_id

	def json(self):
		return { 'name': self.name, 'id': self.id, 'courses': [course.json() for course in self.courses.all()]}

	@classmethod
	def find_by_name(cls, name):
		return cls.query.filter_by(name=name).first()  # SELECT * FROM items WHERE name=name LIMIT 1

	