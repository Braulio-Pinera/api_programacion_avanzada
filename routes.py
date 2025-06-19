#El archivo almacena rutas del servidor
from flask import Flask, Response, render_template, request, redirect, url_for, make_response
from models import PeliculaSerie, Calificacion, Comentario, Usuario
from methods import crear_cuenta, iniciar_sesion, encontrar_usuario_por_id, crear_calificacion, crear_comentario, crear_contenido

from flask_jwt_extended import decode_token, verify_jwt_in_request, get_jwt_identity

firma = '8fRVMkuaOY9mVec40V7Igl6vu93FEx'

def cargar_rutas(app):
    @app.route('/')
    def inicio():
        
        access_token = request.cookies.get('access_token')
        datos_usuario = obtener_info_usuario()
        
        if access_token == None or access_token == '':
            return render_template('index.html')
        elif datos_usuario['user_type'] == 'estandar':
            print('Usuario estandar')
            id=obtener_id_usuario()
            contenidos = PeliculaSerie.query.all()
            calificaciones_usuario = Calificacion.query.filter_by(usuario_id=datos_usuario['id']).all()
            calif_dict = {c.peliculas_series_id: c.puntuacion for c in calificaciones_usuario}
            return render_template('perfil_estandar.html', contenidos=contenidos, calificaciones=calif_dict)
        elif datos_usuario['user_type'] == 'moderador':
            print('Usuario moderador')
            id=obtener_id_usuario()
            contenidos = PeliculaSerie.query.all()
            calificaciones_usuario = Calificacion.query.filter_by(usuario_id=datos_usuario['id']).all()
            calif_dict = {c.peliculas_series_id: c.puntuacion for c in calificaciones_usuario}
            return render_template('perfil_moderador.html', contenidos=contenidos, calificaciones=calif_dict)

    @app.route('/login')
    def login():
        resultado = request.args.get('status')

        return render_template('login.html', estado=resultado)

    @app.route('/signup')
    def signup():

        resultado = request.args.get('status')

        return render_template('signup.html', estado=resultado)

    #Esta ruta va a manejar la info
    @app.route('/manipulacion_login', methods=['POST'])
    def manipular_datos_login():
        email = request.form.get('email')
        password = request.form.get('password')
        print(f'''
        Correo: {email}    
        Constraseña: {password}    
    ''')
        respuesta_login = iniciar_sesion(email, password)

        print(respuesta_login)

        if respuesta_login['status'] == 'error1':
            return redirect(url_for('login', status = respuesta_login['status']))
        elif respuesta_login['status'] == 'error2':
            return redirect(url_for('login', status = respuesta_login['status']))
        
        #Si lo de arriba no se cumple, significa que tenemos un token
        respuesta = make_response(redirect(url_for('inicio')))
        respuesta.set_cookie('access_token', respuesta_login['token'], secure=True, max_age=180)
        return respuesta
        
    @app.route('/manipulacion_signup', methods=['POST'])
    def manipular_datos_signup():
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        user_type = request.form.get('role')

        print(f'''
        Nombre: {name}  
        Correo: {email}    
        Constraseña: {password}
        Tipo de usuario: {user_type}    
    ''')
        
        respuesta_signup = crear_cuenta(name, email, password, user_type)

        print(respuesta_signup)

        if respuesta_signup['status'] == 'error':
            return redirect(url_for('signup', status = respuesta_signup['status']))

        return redirect(url_for('login')) 

    
    @app.route('/usuario')
    def pantalla_usuario():
        try:
            verify_jwt_in_request()

            return render_template('user.html')
        
        except Exception as error:
            print('La cookie no existe o está mal')
            print(f'La razón es: {error}')
            return redirect(url_for('login'))

    @app.route('/logout')
    def logout():
        respuesta = make_response(redirect(url_for('inicio')))
        respuesta.set_cookie('access_token', '')
        return respuesta

    @app.route('/crear_contenido')
    def crear_series():
        return render_template('crear.html')
    
    @app.route('/comentar', methods=['POST'])
    def comentar():
        id_usuario = obtener_id_usuario()
        texto = request.form.get("texto")
        contenido_id = request.form.get("contenido_id")
        comentario = crear_comentario(contenido_id, texto, id_usuario)
        print(comentario)
        if comentario['status'] == 'error':
            return redirect(url_for('inicio', status = comentario['status']))     
        return redirect(url_for("inicio"))
                        
    @app.route('/comentar/<int:contenido_id>', methods=["GET", "POST"])
    def comentar_manipular(contenido_id):
        contenido = PeliculaSerie.query.filter_by(id=contenido_id).first()
        return render_template('comentar.html', contenido=contenido)

    @app.route('/nuevo_contenido', methods=['POST'])
    def nuevo_contenido():
        id_usuario = obtener_id_usuario()
        datos_usuario = Usuario.query.filter_by(id=id_usuario).first()
        if datos_usuario.user_type != 'moderador':
            return 'Acceso no autorizado', 403
        crear_contenido(request.form, id_usuario)
        return redirect(url_for('inicio'))
    
    @app.route('/calificar/<int:contenido_id>', methods=["GET", "POST"])
    def calificar_manipular(contenido_id):
        contenido = PeliculaSerie.query.filter_by(id=contenido_id).first()
        return render_template('calificar.html', contenido=contenido)

    @app.route('/calificar', methods=['POST'])
    def calificar():
        id_usuario = obtener_id_usuario()
        puntuacion = request.form.get("puntuacion")
        contenido_id = request.form.get("contenido_id")
        calificacion = crear_calificacion(contenido_id, puntuacion, id_usuario)
        print(calificacion)
        if calificacion['status'] == 'error':
            return redirect(url_for('inicio', status = calificacion['status']))  
        return redirect(url_for("inicio"))

    @app.route('/perfil')
    def perfil():
        id_usuario = obtener_id_usuario()
        datos_usuario = Usuario.query.filter_by(id=id_usuario).first()
        return render_template('perfil.html', usuario=datos_usuario)
    
def verificar_autenticacion():
    try:
        verify_jwt_in_request()
        return True
    except:
        return False
    
def obtener_info_usuario():
    try:
        verify_jwt_in_request()
            
        user_token = request.cookies.get('access_token')
        token_info = decode_token(user_token)
            
        id_usuario = token_info['user_id']
        datos_usuario = encontrar_usuario_por_id(id_usuario)
        info_usuario = {'id':datos_usuario.id, 'name':datos_usuario.name, 'email':datos_usuario.email, 'user_type':datos_usuario.user_type}
        return info_usuario
        
    except Exception as error:
        print(error)
        return redirect(url_for('inicio'))

def obtener_id_usuario():
            
    user_token = request.cookies.get('access_token')
    token_info = decode_token(user_token) 
    id_usuario = token_info['user_id']
    id = id_usuario
    return id

#lista_usuarios = encontrar_todos_los_usuarios()
        
        #print(lista_usuarios[0].name)
        #for usuario in lista_usuarios:
            #print(f'''
        #nombre usuario: {usuario.name}          
        #correo usuario: {usuario.email}
        #contraseña usuario: {usuario.password}
        #tipo de usuario: {usuario.user_type}          
#''')