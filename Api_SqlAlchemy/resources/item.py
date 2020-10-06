from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('price', 
		type=float, 
		required=True, 
		help="This field cannot be left blank!")
	parser.add_argument('store_id', 
		type=int, 
		required=True, 
		help="è necessario uno store_id per ogni item")

	@jwt_required() #questo decoratore impone che il client sia autenticato per poter chiamare la get. Per aunticarsi la request deve avere tra gli header anche l'header "Authentication" con valore: JWT <token ricevuto con post a /auth con json con username e password>
	def get(self,name):
		item=ItemModel.find_by_name(name)
		if item:
			return item.json()
		return {'message': 'item not found'}, 404

	def post(self,name):
		if ItemModel.find_by_name(name):
			return {'message':f"l'item {name} esiste già in memoria e non può essere aggiunto"} , 400
		else:
			data = Item.parser.parse_args()
			item=ItemModel(name, data['price'], data['store_id'])
		try:
			item.save_to_db()
		except:
			return {"message": "errore nell'inserimento dell'item"}, 500
		return item.json(), 201

	@jwt_required()
	def delete(self,name):
		item=ItemModel.find_by_name(name)
		if item:
			item.delete_from_db()
		return {"message": "item cancellato"}

	def put(self, name):
		data = Item.parser.parse_args()
		item = ItemModel.find_by_name(name)

		if item is None:
			item=ItemModel(name, data['price'], data['store_id'])
		else:
			item.price=data['price']
		item.save_to_db()

		return item.json() 
		

class ItemList(Resource):
	def get(self):
		return {'items': [i.json() for i in ItemModel.query.all()]}
