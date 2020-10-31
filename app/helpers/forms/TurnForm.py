from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
from wtforms.widgets import HiddenInput
from wtforms.fields.html5 import EmailField, DateTimeField
from wtforms.validators import DataRequired, Email


class TurnForm(FlaskForm):

    id = IntegerField(widget=HiddenInput(), default=20)
    email = EmailField('Correo Electrónico',
                       validators=[DataRequired(), Email()])
    day_hour = DateTimeField('Fecha y hora del turno',
                             validators=[DataRequired()])

    submit = SubmitField('Enviar')
