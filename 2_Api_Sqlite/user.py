import sqlite3
from flask_restful import Resource, reqparse



class User:
	def __init__(self, _id, username, password):
		self.id=_id
		self.username=username
		self.password=password

	@classmethod
	def find_by_username(cls, username):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query="SELECT * FROM users WHERE username=?"
		result = cursor.execute(query,(username,)) #i parametri devono sempre essere espressi in tuple, per quello c'è (username,)
		row = result.fetchone()
		if row: #se la query mi resituisce 0 righe row è None
			user=cls(*row) #chiuso il costruttore di User espandendo tutti gli argomenti (l'ordine deve essere quello giusto, row[0] deve essere l'id, row[1] deve essere lo username e row[2] la password)
		else: 
			user = None

		connection.close()
		return user

	@classmethod
	def find_by_id(cls, _id):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query="SELECT * FROM users WHERE id=?"
		result = cursor.execute(query,(_id,)) #i parametri devono sempre essere espressi in tuple, per quello c'è (username,)
		row = result.fetchone()
		if row: #se la query mi resituisce 0 righe row è None
			user=cls(*row) #chiuso il costruttore di User espandendo tutti gli argomenti (l'ordine deve essere quello giusto, row[0] deve essere l'id, row[1] deve essere lo username e row[2] la password)
		else: 
			user = None

		connection.close()
		return user


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
		if not User.find_by_username(data['username']):

			connection= sqlite3.connect('data.db')
			cursor = connection.cursor()

			query="INSERT INTO users VALUES (NULL,?,?)" #il primo è nullo perchè è l'id. i due "?" sono per username e password
			cursor.execute(query,(data['username'], data['password']))

			connection.commit()
			connection.close()

			return {'message': 'User created successfully'}, 201
		else:
			return {'message': 'user already present'}, 400