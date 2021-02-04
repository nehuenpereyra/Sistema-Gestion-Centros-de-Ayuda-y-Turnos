
from wtforms import RadioField
from wtforms.validators import DataRequired

from app.helpers.forms.HelpCenterForm import HelpCenterForm

class HelpCenterCreateForm(HelpCenterForm):

    request_status = RadioField('',
        choices=[('pending', 'Pendiente'), ('accepted', 'Aceptado')],
        validators=[DataRequired()]
    )
