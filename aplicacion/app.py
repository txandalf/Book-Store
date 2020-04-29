from flask import Flask, render_template, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from aplicacion import config
from werkzeug.utils import secure_filename
import os
from aplicacion.forms import formGenero, formArticulo


app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)


# Una vez instanciado el objeto db, importamos los modelos
from aplicacion.models import Generos, Articulos

#   Podemos acceder con '/' para mostrar todos los libros(genero todos, id=0)
#   o podemos acceder por '/genero/id y mostrar libros por genero

@app.route('/')
@app.route("/genero/<id>")              #<id>, los <> es para indicar un número
def inicio(id='0'):                     # El id por defecto es 0, de ese modo mostramos todos los libros
    genero = Generos.query.get(id)
    if id == '0':
        articulos = Articulos.query.all()
    else:
        articulos = Articulos.query.filter_by(GeneroId=id) # por relación sería genero=genero
    generos = Generos.query.all()
    return render_template("inicio.html", genero=genero, articulos=articulos, generos=generos)


@app.route("/generos")
def generos():
    generos = Generos.query.all()
    return render_template("generos.html", generos=generos)


@app.route("/generos/new", methods=["GET", "POST"]) # Si es get, mostramos el formulario
def generos_new():                                  # si es post, guardamos los registros
    form = formGenero()
    if form.validate_on_submit():
        #POST
        genero = Generos(nombre=form.nombre.data)
        db.session.add(genero)
        db.session.commit()
        return redirect(url_for("generos"))

    return render_template("generos_new.html", form=form)   # Cargamos la plantilla para rellenar el form
                                                            # y le pasamos el form que hemos creado

@app.route("/articulos/new", methods=["GET", "POST"])
def articulos_new():
    form = formArticulo()
    # Inicializamos el selector de genero del form
    generos = [(g.id, g.nombre) for g in Generos.query.all()[1:]]# Desde el 1, para no añadir el Todos con id=0
    form.GeneroId.choices = generos
    if form.validate_on_submit():
        try:
            f = form.photo.data
            nombre_fichero = secure_filename(f.filename)
            f.save(app.root_path + "/static/upload/" + nombre_fichero)
        except:
            nombre_fichero = ""

        art = Articulos()
        form.populate_obj(art)
        art.image = nombre_fichero  # Añadimos el campo que nos falta, por el try...
        db.session.add(art)
        db.session.commit()
        return redirect(url_for("inicio"))

    else:
        return render_template("articulos_new.html", form=form)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", error="Aquí no hay nada..."), 404
