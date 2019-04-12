from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.uni import UniModel

class Uni(Resource):
	parser = reqparse.RequestParser()
	
	parser.add_argument('bundesland_id',
		type=int,
		required=True,
		help="Items require a Bundesland ID."
	)

	
	def get(self, bundesland, uni):
		uni = UniModel.find_by_name(uni)
		if uni:
			return uni.json()
		return {'message': 'Universität wurde nicht gefunden.'}, 404
	
	@jwt_required()	
	def post(self, bundesland, uni):
		if UniModel.find_by_name(uni):
			return {'message': 'Eine Universität mit dem Namen \'{}\' ist bereits vorhanden.'.format(uni)}, 400

		data = Uni.parser.parse_args()
		
		new_uni = UniModel(uni, **data)

		try:
			new_uni.save_to_db()
		except:
			return {'message': 'Ein Fehler ist aufgetreten.'}, 500

		return new_uni.json(), 201

	def delete(self, bundesland, uni):
		del_uni = UniModel.find_by_name(uni)
		if del_uni:
			del_uni.delete_from_db()

		return {'message': 'Universtität wurde gelöscht.'}


class UniList(Resource):
	def get(self, bundesland):
		data = Uni.parser.parse_args()

		return {'unis': [uni.json() for uni in UniModel.query.filter_by(**data)]}
		# alt: return {'unis': list(map(lambda x: x.json(), UniModel.query.all()))}