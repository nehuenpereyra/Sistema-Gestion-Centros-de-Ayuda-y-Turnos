from flask import redirect, render_template, request, url_for, abort
from flask_login import login_required

from app.helpers.permission import permission
from app.helpers.forms.ConfigurationForm import ConfigurationForm
from app.helpers.alert import add_alert
from app.models.configuration import Configuration
from app.models.alert import Alert


@login_required
@permission('configuration_update')
def edit():
    config = Configuration.query.all()[0]
    form = ConfigurationForm(obj=config)
    return render_template("configuration/update.html", form=form)


@login_required
@permission('configuration_update')
def update():
    form = ConfigurationForm()
    if form.validate_on_submit():
        config = Configuration.query.all()[0]
        config.title = form.title.data
        config.description = form.description.data
        config.contact_email = form.contact_email.data
        config.pagination_elements = form.pagination_elements.data
        config.enabled_site = form.enabled_site.data
        config.save()
        add_alert(
            Alert("success", f"La configuración se actualizo correctamente."))
        return redirect(url_for("index"))
    return render_template("configuration/update.html", form=form)
