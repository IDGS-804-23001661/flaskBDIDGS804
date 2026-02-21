from wtforms import Form
from flask_wtf import FlaskForm
 
from wtforms import StringField, IntegerField
from wtforms import EmailField
from wtforms import validators
 
class UserForm(Form):
    id = IntegerField('id', [
        validators.number_range(min=1, max=20, message='valor no valido')
    ])
   
    nombre = StringField('nombre', [
        validators.DataRequired(message='El nombre es requerido'),
        validators.length(min=4, max=20, message='requiere min=4 max=20')
    ])
   
    apellidos = StringField('apellidos', [
        validators.DataRequired(message='Los apellidos son requeridos')
    ])
   
    email = EmailField('correo', [
        validators.DataRequired(message='El correo es requerido'),
        validators.Email(message='Ingrese un correo valido')
    ])

    telefono = StringField('telefono', [
        validators.DataRequired(message='El telefono es requerido')
    ])
