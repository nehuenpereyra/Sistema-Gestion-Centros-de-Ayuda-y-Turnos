
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

    return render_template("help_center/show.html", help_center=help_center, alert=get_alert())


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


@login_required
@permission('help_center_certify')
def accept(id):
    help_center = HelpCenter.query.get(id)

    if not help_center:
        add_alert(Alert("danger", "El centro de ayuda no existe"))
        return redirect(url_for("help_center_index"))

    if not help_center.is_in_pending_state():
        add_alert(Alert(
            "danger", f"El centro de ayuda se encuentra actualmente {help_center.request_status}"))
        return redirect(url_for("help_center_show", id=id))

    help_center.accept_request()
    help_center.save()

    add_alert(Alert("success", "El centro de ayuda fue aceptado con exito"))
    return redirect(url_for("help_center_show", id=id))


@login_required
@permission('help_center_certify')
def reject(id):
    return "ok"


@login_required
@permission('help_center_certify')
def certify(id, is_accepted):
    help_center = HelpCenter.query.get(id)

    if not help_center:
        add_alert(Alert("danger", "El centro de ayuda no existe"))
        return redirect(url_for("help_center_index"))

    center_state_message = {
        False: "rechazado",
        True: "aceptado"
    }

    if not help_center.is_in_pending_state():
        add_alert(Alert(
            "danger", f"El centro de ayuda se encuentra actualmente {center_state_message[help_center.is_in_accepted_state()]}"))
        return redirect(url_for("help_center_show", id=id))

    if is_accepted:
        help_center.accept_request()
    else:
        help_center.reject_request()

    help_center.save()

    add_alert(Alert(
        "success", f"El centro de ayuda fue {center_state_message[is_accepted]} con exito"))
    return redirect(url_for("help_center_show", id=id))
