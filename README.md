# PopcornHour

PopcornHour es una aplicación web desarrollada con Flask que permite a los usuarios registrarse, iniciar sesión, ver y crear contenido multimedia (películas y series), calificar y comentar sobre ellos. Cuenta con roles de usuario (estándar y moderador) para diferentes permisos.

---

## Características principales

- Registro y autenticación de usuarios usando JWT almacenados en cookies.
- Dos tipos de usuarios: **estándar** y **moderador**.
- Visualización de contenido multimedia con detalles y comentarios.
- Creación de contenido (solo moderadores).
- Calificación de contenido, permitiendo actualizar calificaciones existentes.
- Comentarios asociados a cada contenido.
- Seguridad básica con JWT y roles.

---

## Tecnologías usadas

- Python 3.x
- Flask
- Flask-JWT-Extended
- Flask-SQLAlchemy
- PostgreSQL
- Werkzeug (para manejo de contraseñas)

---

## Instalación

1. Clona este repositorio:

```bash
git clone <url-del-repositorio>
cd <nombre-del-repositorio>
Crea un entorno virtual e instala dependencias:

bash
Copiar
Editar
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

pip install -r requirements.txt
Configura la base de datos PostgreSQL y actualiza la URI en app.py:

python
Copiar
Editar
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://usuario:contraseña@host:puerto/base_de_datos'
Inicializa la base de datos (asegúrate de tener creada la base):

bash
Copiar
Editar
flask shell
>>> from extensions import db
>>> db.create_all()
>>> exit()
Uso
Ejecuta la aplicación:

bash
Copiar
Editar
python app.py
Abre tu navegador en http://localhost:8000

Regístrate como usuario estándar o moderador.

Explora el contenido, califica, comenta y (si eres moderador) crea nuevo contenido.

Estructura del proyecto
graphql
Copiar
Editar
.
├── app.py                 # Archivo principal que inicializa la app y carga rutas
├── routes.py              # Define las rutas y controladores Flask
├── models.py              # Definición de modelos SQLAlchemy (Usuarios, Contenido, Calificaciones, Comentarios)
├── methods.py             # Lógica para acciones como login, registro, creación de calificaciones/comentarios
├── extensions.py          # Inicialización de extensiones (DB, JWT)
├── templates/             # Plantillas HTML con Jinja2
│   ├── perfil_estandar.html
│   ├── perfil_moderador.html
│   ├── login.html
│   ├── signup.html
│   ├── comentar.html
│   ├── calificar.html
│   └── ...
├── static/                # Archivos estáticos (CSS, JS, imágenes)
└── requirements.txt       # Dependencias del proyecto
Configuración de seguridad
La aplicación usa JWT almacenados en cookies para manejar la sesión.

CSRF está desactivado para facilitar pruebas locales (JWT_COOKIE_CSRF_PROTECTION = False).

No usar la configuración actual de cookies seguras (JWT_COOKIE_SECURE = False) en producción.

Cambia la clave secreta en app.py antes de desplegar.

Notas
Las contraseñas se guardan hasheadas usando Werkzeug.

Los usuarios moderadores pueden crear contenido nuevo.

Las calificaciones se actualizan si el usuario ya calificó ese contenido.

Los comentarios se muestran en el perfil junto con calificaciones.

El token de acceso dura 3 minutos por configuración.

Contribuciones
Si deseas contribuir, crea un fork y abre un Pull Request con tus mejoras.

Licencia
Este proyecto está bajo la licencia MIT.