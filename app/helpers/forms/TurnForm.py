from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, StringField
from wtforms.widgets import HiddenInput
from wtforms.fields.html5 import EmailField, DateTimeField
from wtforms.validators import DataRequired, Email, Length


class TurnForm(FlaskForm):

    id = IntegerField(widget=HiddenInput(), default=20)
    email = EmailField('Correo Electrónico',
                       validators=[DataRequired(), Email()])
    donor_phone_number = StringField(
        'Descripción', validators=[Length(max=90)])
    day_hour = DateTimeField('Fecha y hora del turno',
                             validators=[DataRequired()])

    submit = SubmitField('Enviar')
