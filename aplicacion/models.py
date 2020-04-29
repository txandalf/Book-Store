from sqlalchemy import Boolean, Column, ForeignKey
from sqlalchemy import DateTime, Integer, String, Text, Float
from sqlalchemy.orm import relationship
from aplicacion.app import db

# Modelo de la base de datos

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
