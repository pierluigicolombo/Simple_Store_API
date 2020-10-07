from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource): #questa classe serve a far registrare nuovi utenti. Avrà un endpoint tutto suo
	parser = reqparse.RequestParser()
	parser.add_argument('username', 
		type=str, 
		required=True, 
		help="The field username cannot be left blank!")
	parser.add_argument('password', 
		type=str, 
		required=True, 
		help="The field password cannot be left blank!")


	def post(self):

		data = UserRegister.parser.parse_args()
		if not UserModel.find_by_username(data['username']):

			user=UserModel(**data)
			user.save_to_db()

			return {'message': 'User created successfully'}, 201
		else:
			return {'message': 'user already present'}, 400