from flask import Flask
from flask_restful import Api
from flask_jwt import JWT #serve a firmare i tocken di autenticazione

#da qui abbiamo gli import dei file
from security import authenticate, identity #modulo implementato da me
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from db import db

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key='Drmhze6EPcv0fN_81Bj-nA' #il segreto è necessario per firmare il token di autenticazione. in questo modo un client quando presenta il token di autenticazione il server può verificare che lo abbia firmatto lui stesso
api=Api(app)

jwt=JWT(app, authenticate, identity) #JWT crea un nuovo endpoint /auth. Questo endpoint riceve uno username ed una passwrd e lo manda nella funzione authenticate

@app.before_first_request
def create_tables():
	db.create_all()

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(UserRegister,'/register')

if __name__=='__main__':
	db.init_app(app)
	app.run(port=5000, debug=True)
