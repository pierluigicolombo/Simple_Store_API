from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.store import StoreModel

class Store(Resource):
	
	@jwt_required() 
	def get(self,name):
		store=StoreModel.find_by_name(name)
		if store:
			return store.json()
		return {'message': 'store not found'}, 404


	def post(self,name):
		if StoreModel.find_by_name(name):
			return {'message':f"lo store {name} esiste già in memoria e non può essere aggiunto"} , 400
		else:
			store=StoreModel(name)
		try:
			store.save_to_db()
		except:
			return {"message": "errore nell'inserimento dell'item"}, 500
		return store.json(), 201

	def delete(self, name):
		store=StoreModel.find_by_name(name)
		if store:
			store.delete_from_db()
 
		return {"message": "sore cancellato"}

class StoreList(Resource):
	def get(self):
		return {'stores': [s.json() for s in StoreModel.query.all()]}