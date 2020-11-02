
from flask import url_for, redirect, render_template, request
from flask_login import login_required

from app.helpers.permission import permission
from app.helpers.alert import add_alert, get_alert
from app.helpers.forms.HelpCenterSeekerForm import HelpCenterSeekerForm

from app.models.alert import Alert
from app.models.configuration import Configuration
from app.models.help_center import HelpCenter


@login_required
@permission('help_center_index')
def index():
    search_form = HelpCenterSeekerForm(request.args)

    help_centers = HelpCenter.search(search_query=search_form.search_query.data,
                                     help_center_state=search_form.help_center_state.data,
                                     page=int(request.args.get('page', 1)),
                                     per_page=Configuration.query.first().pagination_elements)

    return render_template("help_center/index.html", help_centers=help_centers, search_form=search_form, alert=get_alert())


@login_required
@permission('help_center_show')
def show(id):
    help_center = HelpCenter.query.get(id)

    if not help_center:
        add_alert(Alert("danger", "El centro de ayuda no existe."))
        return redirect(url_for("help_center_index"))

    return render_template("help_center/show.html", help_center=help_center)


@login_required
@permission('help_center_delete')
def delete(id):
    center = HelpCenter.query.get(id)

    if center:
        center.remove()
        alert = Alert(
            "success", f'El centro de ayuda "{center.name}" fue eliminado con exito.')
    else:
        alert = Alert("danger", "El centro de ayuda no existe.")

    add_alert(alert)
    return redirect(url_for("help_center_index"))
