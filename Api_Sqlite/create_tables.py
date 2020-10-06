#questo file serve solo a creare il file data.db (il database). Si runna una volta sola per creare il database e popolare un po' la tabella principale degli user
import sqlite3

connection= sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)" #creo la tabella se non esiste. Il campo id si autoincrementerà per ogni record inserito
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS items ( name text, price real)" #creo la tabella se non esiste. Il campo id si autoincrementerà per ogni record inserito
cursor.execute(create_table)

connection.commit()
connection.close()