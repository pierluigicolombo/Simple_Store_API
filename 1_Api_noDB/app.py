from flask import Flask, request
from flask_restful import Resource, Api, reqparse #una risorsa è un qualcosa che la nostra Api manipola, inserendola a database o restituendola. Se la nostra Api manipola studenti la nostra risorsa sarà studenti.
from flask_jwt import JWT, jwt_required #serve a firmare i tocken di autenticazione

from security import authenticate, identity #modulo implementato da me

app= Flask(__name__)
app.secret_key='Drmhze6EPcv0fN_81Bj-nA' #il segreto è necessario per firmare il token di autenticazione. in questo modo un client quando presenta il token di autenticazione il server può verificare che lo abbia firmatto lui stesso
api=Api(app)

jwt=JWT(app, authenticate, identity) #JWT crea un nuovo endpoint /auth. Questo endpoint riceve uno username ed una passwrd e lo manda nella funzione authenticate

items=[]
class Item(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('price', 
		type=float, 
		required=True, 
		help="This field cannot be left blank!")

	@jwt_required() #questo decoratore impone che il client sia autenticato per poter chiamare la get. Per aunticarsi la request deve avere tra gli header anche l'header "Authentication" con valore: JWT <token ricevuto con post a /auth con json con username e password>
	def get(self,name):
		results=list(filter(lambda x : x['name']==name,items))
		if len(results)>0:
			return results[0]
		else:
		#se sono qui vuol dire che non trovato l'item e quindi rispondo item non trovato
			return {'name': None, 'price': None} , 404


	def post(self,name):
		results=list(filter(lambda x: x['name']==name,items))
		if len(results)>0:
				return {'message':f"l'item {name} esiste già in memoria e non può essere aggiunto"} , 400
		#qui ci arrivo se nessun item ha quel nome nella lista, quindi lo aggiungo

		data = Item.parser.parse_args()
		item={'name':name, 'price':data['price']}
		items.append(item)

		return data, 201

	@jwt_required()
	def delete(self,name):
		global items
		items=list(filter(lambda x: x['name']!=name,items))
		return {'message': f"l'item {name} è stato eliminato"}

	def put(self, name):
		data = Item.parser.parse_args()
		item = next(filter(lambda x: x['name'] == name, items), None)
		if item is None:
			item = {'name': name, 'price': data['price']}
			items.append(item)
		else:
			item.update(data)
		return item, 201
		

class ItemList(Resource):
	def get(self):
		return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList,'/items')

if __name__=='__main__':
	app.run(port=5000, debug=True)
