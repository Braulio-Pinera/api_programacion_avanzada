#El archivo almacena rutas del servidor
from flask import Flask, render_template, request, redirect, url_for

from methods import crear_cuenta, iniciar_sesion, encontrar_todos_los_usuarios

def cargar_rutas(app):
    @app.route('/')
    def inicio():
        lista_usuarios = encontrar_todos_los_usuarios()
        
        print(lista_usuarios[0].name)
        for usuario in lista_usuarios:
            print(f'''
        nombre usuario: {usuario.name}          
        correo usuario: {usuario.email}
        contraseña usuario: {usuario.password}
        tipo de usuario: {usuario.user_type}          
''')
        return render_template('index.html')

    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')

    @app.route('/login')
    def login():
        return render_template('login.html')

    @app.route('/signup')
    def signup():
        return render_template('signup.html')

    #Esta ruta va a manejar la info
    @app.route('/manipulacion_login', methods=['POST'])
    def manipular_datos_login():
        email = request.form.get('email')
        password = request.form.get('password')

        print(f'''
        Correo: {email}    
        Constraseña: {password}    
    ''')
        iniciar_sesion()

        return redirect(url_for('dashboard'))
        
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
        
        crear_cuenta(name, email, password, user_type)

        return redirect(url_for('login')) 