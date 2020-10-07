'''
QUESTO FILE CONTIENE LA TABELLA DEGLI UTENTI REGISTRATI E ALCUNE FUNZIONI IMPORTANTI PER L'AUTENTICAZIONE
'''
from werkzeug.security import safe_str_cmp #serve per fare il confronto tra la password salvata nel database e quella che ci viene presentata dal client. Se i sistemi e gli encoding sono diversi il paragone == fallisce. QUesta funzione serve a sistemare questo problema
from user import User


def authenticate(username, password):
	user=User.find_by_username(username)
	if user and safe_str_cmp(user.password,password):
		return user

def identity(payload):
	user_id=payload['identity']
	return User.find_by_id(user_id)