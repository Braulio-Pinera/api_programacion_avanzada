#Archivo evita importaciones cirulares
from flask_sqlalchemy import SQLAlchemy
#JWTManager es una clase que, a través de atributos y métodos, 
# controla los procesos para generar JWTs y utilizarlos
from flask_jwt_extended import JWTManager

db = SQLAlchemy()

jwt = JWTManager()