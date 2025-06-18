#El archivo almacena rutas del servidor
from flask import Flask, render_template, request, redirect, url_for, make_response

from methods import crear_cuenta, iniciar_sesion, encontrar_usuario_por_id

from flask_jwt_extended import decode_token, verify_jwt_in_request, get_jwt_identity

firma = '8fRVMkuaOY9mVec40V7Igl6vu93FEx'

def cargar_rutas(app):
    @app.route('/')
    def inicio():
        
        access_token = request.cookies.get('access_token')
        print(f'Esto se imprime: {access_token}')
        datos_usuario = obtener_info_usuario()
        
        if access_token == None or access_token == '':
            return render_template('index.html')
        elif datos_usuario['user_type'] == 'estandar':
            print('Usuario estandar')
            return render_template('dashboard.html', datos_usuario=datos_usuario)
        elif datos_usuario['user_type'] == 'moderador':
            print('Usuario moderador')
            return render_template('dashboard.html', datos_usuario=datos_usuario)

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
    
def obtener_info_usuario():
    try:
        verify_jwt_in_request()
            
        user_token = request.cookies.get('access_token')
        token_info = decode_token(user_token)
            
        id_usuario = token_info['user_id']
        datos_usuario = encontrar_usuario_por_id(id_usuario)
        datos_usuario = {'id':datos_usuario.id, 'name':datos_usuario.name, 'email':datos_usuario.email, 'user_type':datos_usuario.user_type}
        return datos_usuario
        
    except Exception as error:
        print(error)
        return redirect(url_for('inicio'))

#lista_usuarios = encontrar_todos_los_usuarios()
        
        #print(lista_usuarios[0].name)
        #for usuario in lista_usuarios:
            #print(f'''
        #nombre usuario: {usuario.name}          
        #correo usuario: {usuario.email}
        #contraseña usuario: {usuario.password}
        #tipo de usuario: {usuario.user_type}          
#''')