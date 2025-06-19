#Archivo que contiene todas las acciones que un usuario pueda realizar
from models import Usuario, PeliculaSerie, Calificacion, Comentario
from extensions import jwt
from flask_jwt_extended import create_access_token
from datetime import date, timedelta, timezone
from extensions import db

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

def encontrar_pelicula_serie_por_id(pelicula_serie_id):
    pelicula_serie = PeliculaSerie.query.filter_by(id=pelicula_serie_id).first()
    if pelicula_serie == None:
        return {'status': 'Error', 'Error': 'La película no existe en la DB'}
    
    return pelicula_serie

def crear_contenido(formulario, usuario_id):
    nueva_pelicula_serie = PeliculaSerie(
        titulo=formulario['titulo'],
        descripcion=formulario['descripcion'],
        fecha_lanzamiento=date.fromisoformat(formulario['fecha_lanzamiento']),
        tipo=formulario['tipo'],
        genero=formulario['genero'],
        usuario_id=usuario_id
    )

    nueva_pelicula_serie.save()

    return {'status': 'okay', 'nueva_pelicula_serie': nueva_pelicula_serie}

def crear_calificacion(peliculas_series_id, puntuacion, usuario_id):
    calificacion_existente = Calificacion.query.filter_by(
        usuario_id=usuario_id,
        peliculas_series_id=peliculas_series_id
    ).first()

    if calificacion_existente:
        calificacion_existente.puntuacion = puntuacion
        nueva = calificacion_existente.puntuacion
    else:
        nueva = Calificacion(
            usuario_id=usuario_id,
            peliculas_series_id=peliculas_series_id,
            puntuacion=puntuacion
        )
        db.session.add(nueva)
    
    db.session.commit()
    return {'status': 'okay', 'nueva_calificacion': nueva}

def crear_comentario(peliculas_series_id, texto, usuario_id):
    nuevo_comentario = Comentario(
        peliculas_series_id=peliculas_series_id,
        usuario_id=usuario_id,
        texto=texto,
    )

    nuevo_comentario.save()

    return {'status': 'okay', 'nuevo_comentario': nuevo_comentario}