
from flask import url_for, redirect, render_template
from flask_login import login_required

from app.helpers.permission import permission
from app.helpers.alert import add_alert, get_alert

from app.models.alert import Alert
from app.models.help_center import HelpCenter


def index_view(each, result):
    return f"""
        {result}
        <p>
            {each.name}
            - <a href="{url_for("help_center_show", id=each.id)}">Ver</a>
            - <a href="{url_for("help_center_delete", id=each.id)}">Borrar</a>
        </p>
    """


@login_required
@permission('help_center_index')
def index():
    return HelpCenter.query.all().inject(index_view, "")


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
