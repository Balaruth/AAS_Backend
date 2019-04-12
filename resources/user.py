from flask_restful import Resource, reqparse
from models.user import UserModel
from db import db

class UserRegister(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('username',
		type=str,
		required=True,
		help="This field cannot be left blank."
	)

	parser.add_argument('password',
		type=str,
		required=True,
		help="This field cannot be left blank."
	)

	def post(self):
		data = UserRegister.parser.parse_args()

		if UserModel.find_by_username(data['username']):
			return {'message': 'This username has been taken. Please choose another.'}, 409

		user = UserModel(**data)
		db.session.add(user)
		db.session.commit()

		return {'message': 'User created successfully.'}, 201