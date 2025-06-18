from flask import Flask
from routes import cargar_rutas
from extensions import db, jwt

app = Flask(__name__)

#Configuración para conectarse a una DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.lbouwqvcrbzjxzwhdjxl:&-Rz3h!nw%K%$Qg@aws-0-us-west-1.pooler.supabase.com:6543/postgres'
#Desactivar trackeo de modificaciones (innecesario en este proyecto)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Agregamos firma para tokens
app.config['JWT_SECRET_KEY'] = '8fRVMkuaOY9mVec40V7Igl6vu93FEx'

#Le indicamos a la app que el token de acceso estará en las cookies
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token'
app.config['JWT_COOKIE_CSFR_PROTECTION'] = False

#Objeto para controlar DB en python
db.init_app(app)
#Establecemos "conexión" entre jwt y la app
jwt.init_app(app)

cargar_rutas(app)

app.run(port=8000, debug=True)