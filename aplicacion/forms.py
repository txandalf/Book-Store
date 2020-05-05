from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField, HiddenField, IntegerField, TextAreaField, SelectField
from flask_wtf.file import FileField
from wtforms.validators import Required, NumberRange
from wtforms.fields.html5 import EmailField


class formGenero(FlaskForm):
    nombre = StringField("Nombre: ", validators=[Required("Campo <nombre> ncesario")])
    submit = SubmitField("Enviar")


class formArticulo(FlaskForm):
    '''
        Los campos tienen los mismos nombres que nuestro modelo
        de datos, para facilitar la creación de nuevos registros
        pasando como parametro de los nuevos articulos el contenido
        del formulario
    '''
    nombre = StringField("Nombre: ", validators=[Required("Campo <nombre> es necesario")])
    precio = DecimalField("Precio: ", default=0, validators=[Required("Campo <precio> es necesario")])
    iva = IntegerField("IVA: ", default=21, validators=[Required("Campo <IVA> necesario")])
    sinopsis = TextAreaField("Sinopsis: ")
    photo = FileField("Selecciona una imágen")
    stock = IntegerField("Stock: ", default=1, validators=[Required("Campo <stock> necesario")])
    GeneroId = SelectField("Género: ", coerce=int)
    submit = SubmitField("Enviar")

# Creamos los formularios necesarios para la gestoón de los usuarios;
# - Para logearnos
# - Para registrarnos
# - Para cambiar la contraseña

#Login
class formLogin(FlaskForm):
    username = StringField("Usuario", validators=[Required()])
    password = PasswordField("Contraseña", validators=[Required()])
    submit = SubmitField("Entrar")


# Registro
class formUsuario(FlaskForm):
    username = StringField("Usuario", validators=[Required()])
    password = PasswordField("Contraseña", validators=[Required()])
    nombre = StringField("Nombre completo", validators=[Required()])
    email = EmailField("Email")
    submit = SubmitField("Crear")


# Cambiar contraseña
class formChangePassword(FlaskForm):
    password = PasswordField("Contraseña", validators=[Required()])
    submit = SubmitField("Cambiar")

# Formulario para el carrito (obtendremos los datos de las cookies)
# La cookie contendra un id de articulo y su cantidad, al formulario le pasaremos
# los dos datos, solo que el id no lo mostraremos (se pasarsa por debajo por asi decirlo)
class formCarrito(FlaskForm):
    id = HiddenField()
    cantidad = IntegerField('Cantidad', default=1,
                validators=[NumberRange(min=1, message="El valor debe ser positivo"), Required("Campo obligatorio")])
    submit = SubmitField("Aceptar")
