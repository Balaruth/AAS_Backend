from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.studium import StudiumModel

class Studium(Resource):
	parser = reqparse.RequestParser()

	parser.add_argument('inhalt',
		type=str,
		required=True,
		help="Dieses Feld darf nicht leer sein."
	)

	parser.add_argument('fachbereich_id',
		type=int,
		required=True,
		help="Fachbereich ID muss vorhanden sein."
	)

	
	def get(self, bundesland, uni, fachbereich, studium):
		studium = StudiumModel.find_by_name(studium)
		if studium:
			return studium.json()
		return {'message': 'Studium {} wurde nicht gefunden.'.format(studium)}, 404
	
	@jwt_required()	
	def post(self, bundesland, uni, fachbereich, studium):
		if StudiumModel.find_by_name(studium):
			return {'message': 'Ein Studium mit dem Namen \'{}\' ist bereits vorhanden.'.format(studium)}, 400

		data = Studium.parser.parse_args()
		
		new_studium = StudiumModel(studium, **data)

		try:
			new_studium.save_to_db()
		except:
			return {'message': 'Ein Fehler ist aufgetreten.'}, 500

		return new_studium.json(), 201

	def delete(self, bundesland, uni, fachbereich, studium):
		del_studium = StudiumModel.find_by_name(studium)
		if del_studium:
			del_studium.delete_from_db()

		return {'message': 'Studium wurde gelöscht.'}

	def put(self, bundesland, uni, fachbereich, studium):
		data = Studium.parser.parse_args()

		up_studium = StudiumModel.find_by_name(studium)
		
		if up_studium is None:
			up_studium = StudiumModel(name, **data)
		else:
			up_studium.inhalt = data['inhalt']
		
		up_studium.save_to_db()

		return up_studium.json()


class StudiumList(Resource):
	def get(self, bundesland, uni, fachbereich):
		data = Studium.pasrser.parse_args
		return {'studien': [studium.json() for studium in StudiumModel.query.filter_by(**data)]}