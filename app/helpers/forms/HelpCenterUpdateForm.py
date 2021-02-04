
from wtforms import RadioField
from wtforms.validators import Optional

from app.helpers.forms.HelpCenterForm import HelpCenterForm

class HelpCenterUpdateForm(HelpCenterForm):

    request_status = RadioField('',
        choices=[('rejected', 'Rechazado'), ('accepted', 'Aceptado')],
        validators=[Optional()]
    )
