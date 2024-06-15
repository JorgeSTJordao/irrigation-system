from flask import Flask
from smartsprout.models.db import db
from smartsprout import bcrypt, Usuario

def create_db(app: Flask):
    with app.app_context():
        db.drop_all()
        db.create_all()

        #usuários root
        usuarios_root = {
            "Jorge": ["123456", "administrador"],
            "Leandro": ["123456", "estatístico"],
            "Joelton": ["123456", "operador"],
            "Pedro": ["123456", "comum"]
        }


        for key, value in usuarios_root.items():
            if len(usuarios_root[key][0]) >= 6:
                senha_crypt = bcrypt.generate_password_hash(usuarios_root[key][0])
                usuario = Usuario(
                    username=key,
                    senha=senha_crypt,
                    roles=usuarios_root[key][1]
                )

                db.session.add(usuario)
                db.session.commit()
            else:
               print("Erro: ", key, usuarios_root[key])