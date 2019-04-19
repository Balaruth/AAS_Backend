from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.faculty import FacultyModel

class Faculty(Resource):
	parser = reqparse.RequestParser()

	parser.add_argument('uni_id',
		type=int,
		required=True,
		help="Universität ID is required."
	)

	
	def get(self, region, uni, faculty):
		fachbereich = FacultyModel.find_by_name(faculty)
		if fachbereich:
			return fachbereich.json()
		return {'message': 'Fachbereich {} wurde nicht gefunden.'.format(faculty)}, 404
	
	@jwt_required()	
	def post(self, region, uni, faculty):
		if FacultyModel.find_by_name(faculty):
			return {'message': 'Ein Fachbereich mit dem Namen \'{}\' ist bereits vorhanden.'.format(faculty)}, 400

		data = Faculty.parser.parse_args()
		
		new_faculty = FacultyModel(faculty, **data)

		try:
			new_faculty.save_to_db()
		except:
			return {'message': 'Ein Fehler ist aufgetreten.'}, 500

		return new_faculty.json(), 201
		
	def delete(self, region, uni, faculty):
		del_faculty = FacultyModel.find_by_name(faculty)
		if del_faculty:
			del_faculty.delete_from_db()

		return {'message': 'Fachbereich wurde gelöscht.'}


class FacultyList(Resource):
	def get(self, faculty, uni):
		data = Faculty.parser.parse_args()
		return {'faculties': [faculty.json() for faculty in FacultyModel.query.filter_by(**data)]}