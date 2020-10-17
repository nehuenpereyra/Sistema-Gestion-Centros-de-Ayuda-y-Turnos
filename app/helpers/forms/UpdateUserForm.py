
from wtforms import PasswordField, BooleanField
from wtforms.validators import Length, ValidationError

from app.helpers.forms.UserForm import UserForm


def length_or_empty(min, max):

    def _length_or_empty(form, field):

        message = f'Must be between {min} and {max} characters long.'
        length = len(field.data)

        if (length != 0) and (length < min or length > max):
            raise ValidationError(message)

    return _length_or_empty


class UpdateUserForm(UserForm):

    password = PasswordField('Contraseña',
                             validators=[length_or_empty(min=6, max=20)])

    is_active = BooleanField("Activo", default=True)
