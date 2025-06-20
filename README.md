# 🎬 PopcornHour

**PopcornHour** es una plataforma web desarrollada con Flask que permite a los usuarios explorar, calificar y comentar películas y series. Incluye funcionalidades diferenciadas para usuarios estándar y moderadores, autenticación con JWT y una base de datos PostgreSQL.

## 🚀 Funcionalidades principales

- Registro e inicio de sesión seguros con JWT
- Visualización de contenido (películas/series)
- Calificación del contenido (1 a 5 estrellas)
- Comentarios por contenido
- Vistas personalizadas para usuarios estándar y moderadores
- Creación de contenido para moderadores

## 🛠 Tecnologías utilizadas

- **Backend:** Python, Flask, Flask-JWT-Extended, SQLAlchemy
- **Base de datos:** PostgreSQL (Supabase)
- **Frontend:** HTML5, CSS3 (embebido), Jinja2
- **Autenticación:** JSON Web Tokens (JWT), cookies seguras

## 🔒 Consideraciones de seguridad

- La aplicación usa JWT almacenados en cookies para manejar la sesión.
- CSRF está desactivado para facilitar pruebas locales (JWT_COOKIE_CSRF_PROTECTION = False).
- No usar la configuración actual de cookies seguras (JWT_COOKIE_SECURE = False) en producción.
- Cambia la clave secreta en app.py antes de desplegar.

## 📌 Mejoras futuras
- Buscador de contenido
- Paginación de resultados
- Gestión avanzada de usuarios (bloqueo, reportes)