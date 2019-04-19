from superclass import Superclass

class RegionModel(db.Superclass):
	__tablename__ = 'regions'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20))

	unis = db.relationship('UniModel', lazy='dynamic')  # back reference to Item Model

	def __init__(self, name):
		self.name = name

	# because of lazy=dynamic self.items is a query builder and not a list, so method all is needed
	def json(self):
		return { 'name': self.name, 'id': self.id, 'unis': [uni.json() for uni in self.unis.all()] }

	@classmethod
	def find_by_name(cls, name):
		return cls.query.filter_by(name=name).first()  # SELECT * FROM items WHERE name=name LIMIT 1