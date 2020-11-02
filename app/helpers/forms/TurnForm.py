from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, StringField
from wtforms.widgets import HiddenInput
from wtforms.fields.html5 import EmailField, DateTimeLocalField
from wtforms.validators import DataRequired, Email, Length
from wtforms.validators import ValidationError


def time_range(min, max):
    def _time_range(form, field):

        message = f'Debe ser un horario entre las {min} y antes de las {max} horas.'
        time = field.data.time()

        if (time.hour < min or time.hour >= max):
            raise ValidationError(message)

    return _time_range


def time_exact():
    def _time_exact(form, field):
        message = f'Debe se ingresar una hora en punto o y media.'
        time = field.data.time()

        if (time.minute != 0 and time.minute != 30):
            raise ValidationError(message)

    return _time_exact


def time_invalid():
    def _time_invalid(form, field):
        message = f'Esa fecha no es valida.'

        if field.data <= datetime.today():
            raise ValidationError(message)

    return _time_invalid


class TurnForm(FlaskForm):

    id = IntegerField(widget=HiddenInput(), default=20)
    email = EmailField('Correo Electrónico',
                       validators=[DataRequired(), Email()])
    donor_phone_number = StringField(
        'Telefono del donante', validators=[Length(max=90)])
    day_hour = DateTimeLocalField('Fecha y hora del turno',  format='%Y-%m-%dT%H:%M',
                                  validators=[DataRequired(), time_range(min=9, max=16), time_exact(), time_invalid()])

    submit = SubmitField('Guardar')
