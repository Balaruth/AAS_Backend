from flask_restful import Resource
from models.region import RegionModel

class Region(Resource):
	def get(self, region):
		region = RegionModel.find_by_name(region)
		if region:
			return region.json()
		return {'message': 'Bundesland wurde nicht gefunden!'}, 404

	def post(self, region):
		if RegionModel.find_by_name(region):
			return {'message': 'Bundesland \'{}\' wurde bereits angelegt.'.format(region)}, 400

		new_region = RegionModel(region)

		try:
			new_region.save_to_db()
		except:
			return {'message': 'Ein fehler ist aufgetreten.'}, 500

		return new_region.json(), 201

	def delete(self, region):
		del_region = RegionModel.find_by_name(region)
		if del_region:
			region.delete_from_db()

		return {'message': 'Bundesland wurde gelöscht.'}

class RegionList(Resource):
	def get(self):
		return {'regions': [region.json() for region in RegionModel.query.all()]}