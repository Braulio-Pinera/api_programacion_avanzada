#Archivo que contiene todas las acciones que un usuario pueda realizar
from models import Usuario


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

    return {'status': 'ok', 'email': email}

def iniciar_sesion(email, password):
    #Que contenga usuarios filtrados a través de un parámetro
    usuarios_existentes = Usuario.query.filter_by(email=email).first()

    if usuarios_existentes is None:
        print('La cuenta no existe')
        return {'status': 'error1', 'error': 'La cuenta no existe'}
    
    if usuarios_existentes.verificar_password(password_plano = password):
        pass

def encontrar_todos_los_usuarios():
    usuarios = Usuario.query.all()
    print(usuarios)
    return usuarios