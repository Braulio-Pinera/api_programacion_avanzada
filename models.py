from extensions import db
from datetime import datetime, timezone
#Módulo para hashear contraseñas
from werkzeug.security import check_password_hash, generate_password_hash


class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)

    __table_args__ = (
        db.CheckConstraint("user_type IN ('moderador', 'estandar')", name='chk_user_type'),
    )

    contenidos = db.relationship('PeliculaSerie', backref='creador', cascade="all, delete")
    calificaciones = db.relationship('Calificacion', backref='usuario', cascade="all, delete")
    comentarios = db.relationship('Comentario', backref='usuario', cascade="all, delete")

    def hashear_password(self, password_original):
        self.password = generate_password_hash(password_original)

    def verificar_password(self, password_plano):
        return check_password_hash(self.password, password_plano)
    
    def save(self):
        #Crear conexión con DB
        db.session.add(self)
        #Asegurar que los cambios se guarden
        db.session.commit()

    def delete(self):
        #Crear conexión con DB
        db.session.delete(self)
        #Asegurar que los cambios se guarden
        db.session.commit()

class PeliculaSerie(db.Model):
    __tablename__ = 'peliculas_series'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    fecha_lanzamiento = db.Column(db.Date)
    tipo = db.Column(db.String(20), nullable=False)
    genero = db.Column(db.String(100))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        db.CheckConstraint("tipo IN ('pelicula', 'serie')", name='chk_tipo'),
    )

    calificaciones = db.relationship('Calificacion', backref='contenido', cascade="all, delete")
    comentarios = db.relationship('Comentario', backref='contenido', lazy='dynamic', cascade="all, delete")

    def save(self):
        #Crear conexión con DB
        db.session.add(self)
        #Asegurar que los cambios se guarden
        db.session.commit()

    def delete(self):
        #Crear conexión con DB
        db.session.delete(self)
        #Asegurar que los cambios se guarden
        db.session.commit()

class Calificacion(db.Model):
    __tablename__ = 'calificaciones'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='CASCADE'), nullable=False)
    peliculas_series_id = db.Column(db.Integer, db.ForeignKey('peliculas_series.id', ondelete='CASCADE'), nullable=False)
    puntuacion = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        db.CheckConstraint('puntuacion >= 1 AND puntuacion <= 5', name='chk_puntuacion'),
        db.UniqueConstraint('usuario_id', 'peliculas_series_id', name='uq_usuario_contenido')
    )

    def save(self):
        #Crear conexión con DB
        db.session.add(self)
        #Asegurar que los cambios se guarden
        db.session.commit()

    def delete(self):
        #Crear conexión con DB
        db.session.delete(self)
        #Asegurar que los cambios se guarden
        db.session.commit()
    

class Comentario(db.Model):
    __tablename__ = 'comentarios'

    id = db.Column(db.Integer, primary_key=True)
    peliculas_series_id = db.Column(db.Integer, db.ForeignKey('peliculas_series.id', ondelete='CASCADE'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='CASCADE'), nullable=False)
    texto = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def save(self):
        #Crear conexión con DB
        db.session.add(self)
        #Asegurar que los cambios se guarden
        db.session.commit()

    def delete(self):
        #Crear conexión con DB
        db.session.delete(self)
        #Asegurar que los cambios se guarden
        db.session.commit()