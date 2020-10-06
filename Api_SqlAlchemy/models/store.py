from db import db

class StoreModel(db.Model):

	__tablename__='stores'
	id=db.Column(db.Integer, primary_key=True)
	name=db.Column(db.String(80))

	items=db.relationship('ItemModel', lazy='dynamic') #qui la variabile items viene popolata automaticamente tramite la join delle due tabelle con le righe ItemModel che hanno id_store uguale a id nella tabella store. Il lazy=dynamic serve per non fare il calcolo appena crei uno store ma per fare il calcolo degli items solo quando sono richiesti

	def __init__(self, name):
		self.name =name

	def json(self):
		return {'name':self.name, 'items': [i.json() for i in self.items.all()]} #se non avessi usato lazy sarebbe stato suff self.items (perchè avevo una lista). con lazy=dynamic devo fare una query, ed il .all() serve a quello

	@classmethod
	def find_by_name(cls,name):
		return cls.query.filter_by(name=name).first()

	def save_to_db (self): #se io ho l'oggetto self che ho recuperato dal database, quindi con un id, e gli cambio il nome e poi uso questo metodo sto facendo un update! non una insert!
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()