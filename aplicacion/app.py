from flask import Flask, render_template, redirect, url_for, abort, request, session, make_response
from flask_sqlalchemy import SQLAlchemy
from aplicacion import config
from werkzeug.utils import secure_filename
import os
import json
from aplicacion.forms import formGenero, formArticulo, formLogin, formUsuario, formChangePassword, formCarrito
#IMPORTAMOS FLASK_LOGIN PARA EL CONTROL DE USUARIOS
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

# Instanciamos el controlador (manager) flask_login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
# CUando accedemos a un sitio donde no tenemos permisos nos redirige a login

# Una vez instanciado el objeto db, importamos los modelos
from aplicacion.models import Generos, Articulos, Usuarios

#   Podemos acceder con '/' para mostrar todos los libros(genero todos, id=0)
#   o podemos acceder por '/genero/id y mostrar libros por genero

@app.route('/')
@app.route("/genero/<id>")              #<id>, los <> es para indicar una variable
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
@login_required # Si no lo esta, redirige a login
def generos_new():                                  # si es post, guardamos los registros

    # Control de permisos, en este caso solo el admin puede añadir
    if not current_user.is_admin():
        abort(404)

    form = formGenero()
    if form.validate_on_submit():
        #POST
        genero = Generos(nombre=form.nombre.data)
        db.session.add(genero)
        db.session.commit()
        return redirect(url_for("generos"))

    return render_template("generos_new.html", form=form)   # Cargamos la plantilla para rellenar el form
                                                            # y le pasamos el form que hemos creado

@app.route("/generos/<id>/edit", methods=["get", "post"])
@login_required
def generos_edit(id):

    if not current_user.is_admin():
        abort(404)

    genero = Generos.query.get(id)

    if genero is None:
        abort(404)          # Por si pasamos una ruta con id inexistente

    form = formGenero(obj=genero)   # Cargamos el formulario con los datos del genero (como el 'populate_obj()')
                                    # (obtenemos el formulario completo de la categoria)
    if form.validate_on_submit():
        form.populate_obj(genero)
        db.session.commit()
        return redirect(url_for("generos"))
    return render_template("generos_new.html", form=form)



@app.route("/articulos/new", methods=["GET", "POST"])
@login_required
def articulos_new():

    if not current_user.is_admin():
        abort(404)

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


@app.route("/articulos/<id>/edit", methods=["GET", "POST"])
@login_required
def articulos_edit(id):

    if not current_user.is_admin():
        abort(404)

    '''Los mismo que con generos_edit'''
    art = Articulos.query.get(id)
    if art is None:
        abort(404)

    form = formArticulo(obj=art)
    generos = [(g.id, g.nombre) for g in Generos.query.all()[1:]]   # Necesario cargar de nuevo los choices
    form.GeneroId.choices = generos

    if form.validate_on_submit():
        if form.photo.data:
            os.remove(app.root_path + "/static/upload/" + art.image)
            try:
                f = form.photo.data
                nombre_fichero = secure_filename(f.filename)
                f.save(app.root_path + "/static/upload/" + nombre_fichero)
            except:
                nombre_fichero = ""
        else:
            nombre_fichero = art.image

        form.populate_obj(art)
        art.image = nombre_fichero
        db.session.commit()
        return redirect(url_for("inicio"))

    return render_template("articulos_new.html", form=form)


@app.route("/generos/<id>/delete", methods=["GET", "POST"])
@login_required
def generos_delete(id):

    if not current_user.is_admin():
        abort(404)

    genero = Generos.query.get(id)
    if genero is None:
        abort(404)

    db.session.delete(genero)
    db.session.commit()
    return redirect(url_for("generos"))


@app.route("/articulos/<id>/delete", methods=["GET", "POST"])
@login_required
def articulos_delete(id):

    if not current_user.is_admin():
        abort(404)

    articulo = Articulos.query.get(id)
    if articulo is None:
        abort(404)

    if articulo.image != "":
        os.remove(app.root_path + "/static/upload/" + articulo.image)
    db.session.delete(articulo)
    db.session.commit()
    return redirect(url_for("inicio"))


# ############### CONTROL DE USUARIOS LOGIN, REGISTRO ##############

@app.route("/login", methods=["GET", "POST"])
def login():
    # COntrolamos que si ya estamos logeados nos redirija a inicio
    if current_user.is_authenticated:
        return redirect(url_for("inicio"))

    form = formLogin()

    if form.validate_on_submit():
        #POST
        user = Usuarios.query.filter_by(username=form.username.data).first()
        if user != None and user.verify_password(form.password.data):
            login_user(user)    # Logeamos al usuario (ahora es current_user para Flask_Login)
            return redirect(url_for("inicio"))
        # Añadimos en username el error para que aparezca sobre el primer input del formulario
        form.username.errors.append("Usuario o contraseña incorrecta")
    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()    # Flask-login se encarga de desconectar el current_user
    return redirect(url_for("inicio"))


@app.route('/registro', methods=["GET", "POST"])
def registro():

    if current_user.is_authenticated:
        return redirect(url_for("inicio"))

    form = formUsuario()

    if form.validate_on_submit():
        #Comprobamos que no existe el usuario
        existe_usuario = Usuarios.query.filter_by(username=form.username.data).first()

        if existe_usuario == None:
            # Lo registramos
            user = Usuarios()
            form.populate_obj(user)
            user.admin = False
            db.session.add(user)
            db.session.commit()

            return redirect(url_for("inicio"))

        form.username.errors.append("Ese nombre de usuario ya existe")

    return render_template("usuarios_new.html", form=form)


@app.route('/perfil/<username>', methods=["GET", "POST"])
@login_required
def perfil(username):
    user = Usuarios.query.filter_by(username=username).first()
    if user is None:
        abort(404)

    form = formUsuario(obj=user)

    #eliminamos la password
    del form.password
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for("inicio"))

    return render_template("usuarios_new.html", form=form, perfil=True, username=user.username)


@app.route('/changepassword/<username>', methods=["GET", "POST"])
@login_required
def changepassword(username):
    user = Usuarios.query.filter_by(username=username).first()
    if user is None:
        abort(404)

    form = formChangePassword()
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for("inicio"))

    return render_template("changepassword.html", form=form)

####### CONTROLAMOS EL CARRITO DE LA COMPRA #############

@app.route('/carrito/add/<id>', methods=["GET", "POST"])
@login_required
def carrito_add(id):
    articulo = Articulos.query.get(id)
    form = formCarrito()
    form.id.data = id   # Pasamos el id al campo oculto (por debajo, sin mostrar nada...)

    if form.validate_on_submit():
        #POST
        if articulo.stock >= int(form.cantidad.data):
            try:
                datos = json.loads(request.cookies.get(str(current_user.id))) # Obtenemos la cookie de ese user en json
            except:
                datos = []
            actualizar = False

            for dato in datos:
                if dato["id"] == id:    # El articulo ya estaba en el carrito y hay que actualizar la cantidad
                    dato["cantidad"] = form.cantidad.data
                    actualizar = True

            if not actualizar: # Al no estar en el carrito lo añadimos (a las cookies)
                datos.append({"id":form.id.data, "cantidad":form.cantidad.data})
            resp = make_response(redirect(url_for('inicio')))
            resp.set_cookie(str(current_user.id), json.dumps(datos))
            return resp
        form.cantidad.errors.append("No hay articulos suficientes")
    return render_template("carrito_add.html", form=form, articulo=articulo)


@app.route('/carrito')
@login_required
def carrito():
    try:
        datos = json.loads(request.cookies.get(str(current_user.id)))   # Obtenemos la cookie del user activo
    except:
        datos = []
    articulos = []
    cantidades = []
    total = 0

    for articulo in datos:
        articulos.append(Articulos.query.get(articulo["id"]))# La cookie no tiene stock, lo aobtenemos obteniendo el objeto entero
        cantidades.append(articulo["cantidad"])
        total = total + Articulos.query.get(articulo["id"]).precio_final() * articulo["cantidad"]

    articulos = zip(articulos, cantidades) # Crea una lista de tuplas [(a1, b1), (a2, b2), ...]
    return render_template("carrito.html", articulos=articulos, total=total)


@app.route('/carrito_delete/<id>')
@login_required
def carrito_delete(id):
    try:
        datos = json.loads(request.cookies.get(str(current_user.id)))
    except:
        datos = []
    new_datos = []
    for dato in datos:
        if dato["id"] == id:
            new_datos.append(dato)
    resp = make_response(redirect(url_for('carrito')))
    resp.set_cookie(str(current_user.id), json.dumps(new_datos))
    return resp



@app.context_processor  # Variables accesibles desde los templates
def contar_carrito():
    if not current_user.is_authenticated:   # Si no esta logeado el carrito es 0
        return {'num_articulos': 0}
    if request.cookies.get(str(current_user.id))==None: # Si está logeado pero no tiene cookie, su carrito es 0
        return {'num_articulos': 0}
    else:
        datos = json.loads(request.cookies.get(str(current_user.id)))
        return {'num_articulos': len(datos)}


@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", error="Aquí no hay nada..."), 404


# IMPORTANTE !
@login_manager.user_loader  # Indicamos a flask como obtener los usuarios por id
def load_user(user_id):     # para llenar el current_user
    return Usuarios.query.get(str(user_id))
