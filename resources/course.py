from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.course import CourseModel

class Course(Resource):
	parser = reqparse.RequestParser()

	parser.add_argument('content',
		type=str,
		required=True,
		help="This field may not be left empty."
	)

	parser.add_argument('faculty_id',
		type=int,
		required=True,
		help="Fachbereich ID is required."
	)

	
	def get(self, region, uni, faculty, course):
		course = CourseModel.find_by_name(course)
		if course:
			return course.json()
		return {'message': 'Studium {} wurde nicht gefunden.'.format(course)}, 404
	
	@jwt_required()	
	def post(self, region, uni, faculty, course):
		if CourseModel.find_by_name(course):
			return {'message': 'Ein Studium mit dem Namen \'{}\' ist bereits vorhanden.'.format(course)}, 400

		data = Studium.parser.parse_args()
		
		new_course = COurseModel(course, **data)

		try:
			new_course.save_to_db()
		except:
			return {'message': 'Ein Fehler ist aufgetreten.'}, 500

		return new_course.json(), 201

	def delete(self, region, uni, faculty, course):
		del_course = CourseModel.find_by_name(course)
		if del_course:
			del_course.delete_from_db()

		return {'message': 'Studium wurde gelöscht.'}

	def put(self, region, uni, faculty, course):
		data = Course.parser.parse_args()

		up_course = CourseModel.find_by_name(course)
		
		if up_course is None:
			up_course = CourseModel(name, **data)
		else:
			up_course.content = data['content']
		
		up_course.save_to_db()

		return up_course.json()


class CourseList(Resource):
	def get(self, region, uni, faculty):
		data = Course.pasrser.parse_args
		return {'courses': [course.json() for course in CourseModel.query.filter_by(**data)]}