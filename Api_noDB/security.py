'''
QUESTO FILE CONTIENE LA TABELLA DEGLI UTENTI REGISTRATI E ALCUNE FUNZIONI IMPORTANTI PER L'AUTENTICAZIONE
'''
from werkzeug.security import safe_str_cmp #serve per fare il confronto tra la password salvata nel database e quella che ci viene presentata dal client. Se i sistemi e gli encoding sono diversi il paragone == fallisce. QUesta funzione serve a sistemare questo problema
from user import User

#tabella degli utenti
users=[User(1,'bob','asdf')]

#mapping table username->user
username_mapping={n.username: n for n in users}

#mapping table id->user
userid_mapping={n.id : n for n in users}

def authenticate(username, password):
	user=username_mapping.get(username,None)
	if user and safe_str_cmp(user.password,password):
		return user

def identity(payload):
	user_id=payload['identity']
	return userid_mapping.get(user_id,None)