from datetime import datetime
import phonenumbers

from .SpanishForm import SpanishForm
from wtforms import SubmitField, IntegerField, StringField
from wtforms.widgets import HiddenInput
from wtforms.fields.html5 import EmailField, DateTimeLocalField, DateField, TimeField
from wtforms.validators import DataRequired, Email, Length, Optional
from wtforms.validators import ValidationError

from app.models.help_center import HelpCenter


def time_range(min, max):
    def _time_range(form, field):

        message = f'Debe ser un horario entre las {min} y antes de las {max} horas.'
        time = field.data

        if (time.hour < min or time.hour >= max):
            raise ValidationError(message)

    return _time_range


def time_exact():
    def _time_exact(form, field):
        message = f'Debe ingresar una hora en punto o y media.'
        time = field.data

        if (time.minute != 0 and time.minute != 30):
            raise ValidationError(message)

    return _time_exact


def unique():
    def _unique(form, field):
        message = f'Un turno en ese día y horario ya fue reservado.'
        if form.time_turn.data and (HelpCenter.query.get(form.center_id.data).turns.any_satisfy(lambda each: (each.day_hour == datetime.combine(field.data, form.time_turn.data)) and (each.id != form.id.data))):
            raise ValidationError(message)
    return _unique


def date_invalid():
    def _time_invalid(form, field):
        message = f'Esa fecha con ese horario no es valida.'

        if form.time_turn.data and datetime.combine(field.data, form.time_turn.data) <= datetime.today():
            raise ValidationError(message)

    return _time_invalid


def valid_number():
    def _valid_number(form, field):
        message = f'No es un numero valido.'
        try:
            if not (phonenumbers.is_valid_number(phonenumbers.parse(field.data, "AR"))):
                raise ValidationError(message)
        except:
            raise ValidationError(message)

    return _valid_number


class TurnForm(SpanishForm):

    id = IntegerField(widget=HiddenInput())
    center_id = IntegerField(widget=HiddenInput(), default=0)
    email = EmailField('Correo Electrónico',
                       validators=[DataRequired(), Email()])
    name = StringField('Nombre', validators=[Length(max=32)])
    surname = StringField('Apellido',
                          validators=[Length(max=32)])
    donor_phone_number = StringField(
        'Telefono del donante', validators=[Optional(), Length(max=90), valid_number()])
    date_turn = DateField('Fecha', format='%Y-%m-%d',
                          validators=[DataRequired(), date_invalid(), unique()])
    time_turn = TimeField('Horario',  format='%H:%M',
                          validators=[DataRequired(), time_range(min=9, max=16), time_exact()])
    submit = SubmitField('Guardar')
