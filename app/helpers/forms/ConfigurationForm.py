from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email, Length
from wtforms.widgets import TextArea
from wtforms.fields.html5 import EmailField


class ConfigurationForm(FlaskForm):
    title = StringField('Titulo', validators=[DataRequired(), Length(max=30)])
    description = StringField('Descripción', validators=[
                              DataRequired(), Length(max=90)], widget=TextArea())
    contact_email = EmailField('Email de contacto', validators=[
        DataRequired(), Email(), Length(max=30)])
    pagination_elements = IntegerField(
        'Numero de elementos en la paginación', validators=[DataRequired()])
    enabled_site = BooleanField(
        'Sitio habilitado', validators=[DataRequired()])
    submit = SubmitField('Actualizar')
