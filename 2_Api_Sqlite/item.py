import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('price', 
		type=float, 
		required=True, 
		help="This field cannot be left blank!")

	@classmethod
	def find_by_name(cls,name):
		connection=sqlite3.connect("data.db")
		cursor=connection.cursor()

		query="SELECT * FROM items WHERE name=?"
		result=cursor.execute(query,(name,))
		row=result.fetchone()
		connection.close()

		if row:
			return {'item':{'name':row[0], 'price':row[1]}}
		
		return None

	@classmethod
	def insert (cls,item):
		connection=sqlite3.connect("data.db")
		cursor=connection.cursor()

		query="INSERT INTO items values(?,?)"
		cursor.execute(query,(item['name'],item['price']))
		connection.commit()
		connection.close()
	@classmethod
	def update(cls,item):
		connection=sqlite3.connect("data.db")
		cursor=connection.cursor()

		query="UPDATE item set price=? where name=?"
		cursor.execute(query,(item['price'],item['name']))

		connection.commit()
		connection.close()

	@jwt_required() #questo decoratore impone che il client sia autenticato per poter chiamare la get. Per aunticarsi la request deve avere tra gli header anche l'header "Authentication" con valore: JWT <token ricevuto con post a /auth con json con username e password>
	def get(self,name):
		item=self.find_by_name(name)
		if item:
			return item
		return {'message': 'item not found'}, 404


	def post(self,name):
		if self.find_by_name(name):
			return {'message':f"l'item {name} esiste già in memoria e non può essere aggiunto"} , 400
		else:
			data = Item.parser.parse_args()
			item={'name':name, 'price':data['price']}
		try:
			self.insert(item)
		except:
			return {"message": "errore nell'inserimento dell'item"}, 500
		return data, 201

	@jwt_required()
	def delete(self,name):
		connection= sqlite3.connect("data.db")
		cursor= connection.cursor()
		query="DELETE FROM items WHERE name=?"
		cursor.execute(query,(name,))
		connection.commit()
		connection.close()

		return {'message': f"l'item {name} è stato eliminato"}

	def put(self, name):
		data = Item.parser.parse_args()
		item = self.find_by_name(name)
		updated_item = {'name': name, 'price': data['price']}


		if item is None:
			try:
				self.insert(updated_item)
			except:
				return {"message":"errore nell'inserimento dell'item"}, 500
		else:
			try:
				self.updated(updated_item)
			except:
				return {"message": "errore nell'inserimento dell'item"}, 500
		return item, 201
		

class ItemList(Resource):
	def get(self):
		connection=sqlite3.connect("data.db")
		cursor= connection.cursor()
		query="SELECT * FROM items"
		results=cursor.execute(query)

		items=[]
		for row in results:
			items.append({'name':row[0],'price':row[1]})
			#items.append(row)

		return {'items':items}
