from flask_restful import Resource
from models.bundesland import BundeslandModel

class Bundesland(Resource):
	def get(self, bundesland):
		bundesland = BundeslandModel.find_by_name(bundesland)
		if bundesland:
			return bundesland.json()
		return {'message': 'Bundesland wurde nicht gefunden!'}, 404

	def post(self, bundesland):
		if BundeslandModel.find_by_name(bundesland):
			return {'message': 'Bundesland \'{}\' wurde bereits angelegt.'.format(bundesland)}, 400

		new_bundesland = BundeslandModel(bundesland)

		try:
			new_bundesland.save_to_db()
		except:
			return {'message': 'Ein fehler ist aufgetreten.'}, 500

		return new_bundesland.json(), 201

	def delete(self, bundesland):
		del_bundesland = BundeslandModel.find_by_name(bundesland)
		if del_bundesland:
			bundesland.delete_from_db()

		return {'message': 'Bundesland wurde gelöscht.'}

class BundeslandList(Resource):
	def get(self):
		return {'bundeslaender': [bundesland.json() for bundesland in BundeslandModel.query.all()]}