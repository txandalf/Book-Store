from flask_script import Manager
from aplicacion.app import app, db
from aplicacion.models import *
import codecs
import os


manager = Manager(app)
app.config["DEBUG"] = True  # Habilitamos el debgger


@manager.command
def create_tables():
    ''' Cre las tablas de la db relacional'''
    db.create_all()
    generoTodos = Generos(id=0, nombre="Todos")
    db.session.add(generoTodos)
    db.session.commit()

@manager.command
def drop_tables():

    db.drop_all()

@manager.command
def add_data_tables():

    db.create_all()

    generos = ("Fantasía", "Poesía", "Ciencia Ficción", "Ensayo", "Historia")

    for gen in generos:
        genero = Generos(nombre=gen)
        db.session.add(genero)
        db.session.commit()


    sinopsis_list = get_book_sinopsis()

    libros = [
        {"nombre":"El nombre del viento", "precio":10, "sinopsis":sinopsis_list[0], "stock":20, "GeneroId":1, "image":"nowind.jpg"},
        {"nombre":"El temor de un hombre sabio", "precio":10, "sinopsis":sinopsis_list[1], "stock":20, "GeneroId":1, "image":"etduhsabio.jpg"},
        {"nombre":"20 Poemas", "precio":7.95, "sinopsis":sinopsis_list[2], "stock":2, "GeneroId":2, "image":"20pbukowski.jpg"},
        {"nombre":"Dune", "precio":15, "sinopsis":sinopsis_list[3], "stock":6, "GeneroId":3, "image":"dune.jpg"},
        {"nombre":"La ciencia del sexo", "precio":15, "sinopsis":sinopsis_list[4], "stock":3, "GeneroId":4, "image":"lcdsexo.jpg"},
        {"nombre":"La otra historia de los templarios", "precio":22, "sinopsis":sinopsis_list[5], "stock":1, "GeneroId":5, "image":"lohdltemplarios.jpg"},
    ]



    for lib in libros:
        libro = Articulos(**lib)
        db.session.add(libro)
        db.session.commit()

def get_book_sinopsis():
    sinopsis = []
    path = os.getcwd() + "/aplicacion/static/sinopsis"
    for f in os.listdir(path):
        file = open(path+"/"+f, encoding="utf8")
        text = file.read()
        file.close()
        sinopsis.append(text)

    return sinopsis

if __name__ == "__main__":
    manager.run()
