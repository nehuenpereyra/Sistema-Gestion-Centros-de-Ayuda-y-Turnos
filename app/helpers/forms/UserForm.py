from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, IntegerField
from wtforms.widgets import HiddenInput
from wtforms.fields.html5 import EmailField
from wtforms.validators import ValidationError, DataRequired, Email, Length
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField

from app.models.user import User
from app.models.user_role import UserRole


def unique(class_, query_filter):

    def _unique(form, field):

        object_form = class_.query.get(form.id.data)
        object_db = class_.query.filter_by(
            **{query_filter: field.data}).first()

        if object_db and object_db != object_form:
            raise ValidationError(f'The value {field.data} is already loaded')

    return _unique


class UserForm(FlaskForm):

    id = IntegerField(widget=HiddenInput(), default=20)
    name = StringField('Nombre', validators=[DataRequired(), Length(max=20)])
    surname = StringField('Apellido',
                          validators=[DataRequired(), Length(max=20)])
    username = StringField('Nombre de usuario',
                           validators=[DataRequired(), Length(max=20), unique(User, "username")])
    email = EmailField('Correo Electrónico',
                       validators=[DataRequired(), Email(), unique(User, "email")])

    roles = QuerySelectMultipleField("Roles", query_factory=lambda: UserRole.query.all(),
                                     get_label="name", validators=[DataRequired()])

    submit = SubmitField('Enviar')
