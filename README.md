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

## 📦 Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/Braulio-Pinera/api_programacion_avanzada
   cd programacion_avanzada

2. Crea y activa un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt

4. Configura la base de datos:
    
    Asegúrate de que la URI de conexión a PostgreSQL esté correctamente definida en app.py
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.lbouwqvcrbzjxzwhdjxl:&-Rz3h!nw%K%$Qg@aws-0-us-west-1.pooler.supabase.com:6543/postgres'