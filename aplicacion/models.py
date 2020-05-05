from sqlalchemy import Boolean, Column, ForeignKey
from sqlalchemy import DateTime, Integer, String, Text, Float
from sqlalchemy.orm import relationship
from aplicacion.app import db
from werkzeug.security import generate_password_hash, check_password_hash # Buena practica para proteger passwords

# Modelo de la base de datos

class Usuarios(db.Model):
	'''Usuarios de la tienda'''
	__tablename__ = "usuarios"
	id = Column(Integer, primary_key=True)
	username = Column(String(100), nullable=False)
	password_hash = Column(String(128), nullable=False)
	nombre = Column(String(200), nullable=False)
	email = Column(String(200), nullable=False)
	admin = Column(Boolean, default=False)

	def __repr__(self):
		return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

	@property
	def password(self):	# @property de password es el get_password
		return AttributeError("Password is not a readable attribute")

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)	# Ciframos la contraseña
	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	# Integración de Flask-Login
	# Esta info dependera de nuestra base de DATOS
	# y la lógica de nuestros modelos.
	def is_authenticated(self):
		return True

	def is_active(self):	# No tenemos un campo para indicar si un Usuario esta activo,
		return True			# por lo tanto es un valor que siempre es verdadero

	def is_anonymous(self):
		return False

	def get_id(self):
		return str(self.id)

	def is_admin(self):
		return self.admin


class Generos(db.Model):
    '''Géneros de los libros'''
    __tablename__ = "generos"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    articulos = relationship("Articulos", cascade="all, delete-orphan", backref="Generos", lazy="dynamic")


    def __repr__(self):
        return (u"<{self.__class__.__name__}: {self.id}>".format(self=self))

class Articulos(db.Model):
    '''Artículos de la tienda'''
    __tablename__ = "articulos"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    precio = Column(Float, default=0)
    iva = Column(Integer, default=21)
    sinopsis = Column(String(255))
    image = Column(String(255))
    stock = Column(Integer, default=0)
    GeneroId = Column(Integer, ForeignKey("generos.id"), nullable=False)
    genero = relationship("Generos", backref="Articulos")


    def precio_final(self):
        return self.precio + (self.precio * (self.iva/100))

    def __repr__(self):
        return (u"<{self.__class__.__name__}: {self.id}>".format(self=self))
