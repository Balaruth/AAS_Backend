from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.fachbereich import FachbereichModel

class Fachbereich(Resource):
	parser = reqparse.RequestParser()

	parser.add_argument('uni_id',
		type=int,
		required=True,
		help="Universität ID muss vorhanden sein."
	)

	
	def get(self, bundesland, uni, fachbereich):
		fachbereich = FachbereichModel.find_by_name(fachbereich)
		if fachbereich:
			return fachbereich.json()
		return {'message': 'Fachbereich {} wurde nicht gefunden.'.format(fachbereich)}, 404
	
	@jwt_required()	
	def post(self, bundesland, uni, fachbereich):
		if FachbereichModel.find_by_name(fachbereich):
			return {'message': 'Ein Fachbereich mit dem Namen \'{}\' ist bereits vorhanden.'.format(fachbereich)}, 400

		data = Fachbereich.parser.parse_args()
		
		new_fachbereich = FachbereichModel(fachbereich, **data)

		try:
			new_fachbereich.save_to_db()
		except:
			return {'message': 'Ein Fehler ist aufgetreten.'}, 500

		return new_fachbereich.json(), 201

	def delete(self, bundesland, uni, fachbereich):
		del_fachbereich = FachbereichModel.find_by_name(fachbereich)
		if del_fachbereich:
			del_fachbereich.delete_from_db()

		return {'message': 'Fachbereich wurde gelöscht.'}


class FachbereichList(Resource):
	def get(self, bundesland, uni):
		data = Fachbereich.parser.parse_args()
		return {'fachbereiche': [fachbereich.json() for fachbereich in FachbereichModel.query.filter_by(**data)]}