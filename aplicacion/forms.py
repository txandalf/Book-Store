from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, IntegerField, TextAreaField, SelectField
from flask_wtf.file import FileField
from wtforms.validators import Required


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
