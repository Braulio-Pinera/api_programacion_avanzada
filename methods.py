#Archivo que contiene todas las acciones que un usuario pueda realizar
from models import Usuario, PeliculaSerie, Calificacion, Comentario
from extensions import jwt
from flask_jwt_extended import create_access_token
from datetime import date, timedelta

def crear_cuenta(name, email, password, user_type):
    #Crear objeto tipo usuario que contendrá info para DB
    usuario_existente = Usuario.query.filter_by(email=email).first()

    if usuario_existente is not None:
        print('El correo ya existe en la DB')
        return {'status': 'error', 'error': 'La cuenta ya está registrada'}

    nuevo_usuario = Usuario(name=name, email=email, user_type=user_type)

    nuevo_usuario.hashear_password(password_original=password)
    #Guardar objeto en db
    nuevo_usuario.save()

    return {'status': 'okay', 'nuevo_usuario': nuevo_usuario}

def iniciar_sesion(email, password):
    #Que contenga usuarios filtrados a través de un parámetro
    usuarios_existentes = Usuario.query.filter_by(email=email).first()

    if usuarios_existentes is None:
        print('La cuenta no existe')
        return {'status': 'error1', 'error': 'La cuenta no existe'}
    
    if usuarios_existentes.verificar_password(password_plano = password):
        caducidad = timedelta(minutes=3)

        print('Inicio de sesión exitoso')
        token_de_acceso = create_access_token(identity=usuarios_existentes.name, expires_delta=caducidad, additional_claims={'user_id': usuarios_existentes.id, 'user_type': usuarios_existentes.user_type})
        print(token_de_acceso)
        return {'status': 'okay', 'token': token_de_acceso}
    else:
        print('Contraseña incorrecta')
        return {'status': 'error2', 'error': 'Contraseña incorrecta'}

#def encontrar_todos_los_usuarios():
    usuarios = Usuario.query.all()
    print(usuarios)
    return usuarios

def encontrar_usuario_por_id(user_id):
    usuario = Usuario.query.filter_by(id=user_id).first()
    if usuario == None:
        return {'status': 'Error', 'Error': 'El usuario no existe en la DB'}
    
    return usuario

def crear_contenido(titulo, descripcion, fecha_lanzamiento, tipo, genero, creado_por_id):
    nuevo_contenido = PeliculaSerie(
        titulo=titulo,
        descripcion=descripcion,
        fecha_lanzamiento=fecha_lanzamiento,
        tipo=tipo,
        genero=genero,
        creado_por=creado_por_id
    )
