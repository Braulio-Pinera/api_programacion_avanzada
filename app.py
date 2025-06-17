from flask import Flask
from routes import cargar_rutas
from extensions import db

app = Flask(__name__)

#Configuración para conectarse a una DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.lbouwqvcrbzjxzwhdjxl:&-Rz3h!nw%K%$Qg@aws-0-us-west-1.pooler.supabase.com:6543/postgres'
#Desactivar trackeo de modificaciones (innecesario en este proyecto)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
#Objeto para controlar DB en python


cargar_rutas(app)

app.run(port=8000, debug=True)