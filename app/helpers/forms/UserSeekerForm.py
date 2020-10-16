
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired


class UserSeekerForm(FlaskForm):
    data_seeker = StringField('Buscar')
    user_state = RadioField(
        '', choices=[('active', 'Activos'), ('blocked', 'Bloqueados')])
    submit = SubmitField('Buscar')
