from superclass import Superclass


class UniModel(Superclass):
	__tablename__ = 'unis'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))

	region_id = db.Column(db.Integer, db.ForeignKey('regions.id'))  # foreign key tablename.columnname
	region = db.relationship('RegionModel')  # same functionality as a SQL Join
	faculties = db.relationship('FacultyModel', lazy='dynamic') 

	def __init__(self, name, region_id):
		self.name = name
		self.region_id = region_id

	def json(self):
		return { 'name': self.name, 'id': self.id, 'faculties': [faculty.json() for faculty in self.faculties.all()] }

	@classmethod
	def find_by_name(cls, name):
		return cls.query.filter_by(name=name).first()  # SELECT * FROM items WHERE name=name LIMIT 1