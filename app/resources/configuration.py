from flask import redirect, render_template, request, url_for, abort
from app.models.configuration import Configuration
from app.helpers.forms.ConfigurationForm import ConfigurationForm
from flask_login import login_required


@login_required
def edit():
    config = Configuration.query.all()[0]
    form = ConfigurationForm(obj=config)
    return render_template("configuration/update.html", form=form)

@login_required
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
        return redirect(url_for("index"))  
    return render_template("configuration/update.html", form=form)