from flask import redirect, render_template, request, url_for, abort
from flask_login import login_user, login_required, current_user

from app.models.turn import Turn
from app.models.alert import Alert
from app.models.help_center import HelpCenter
from app.helpers.forms.TurnForm import TurnForm
from app.helpers.permission import permission
from app.helpers.alert import add_alert


@login_required
@permission('user_create')
def new(id):
    return render_template("turn/new.html", turn_id=id, form=TurnForm())


@login_required
@permission('user_create')
def create(id):
    form = TurnForm()
    print(form.email.data)
    print(form.day_hour.data)
    if form.validate_on_submit():
        Turn(help_center=HelpCenter.query.get(id),
             email=form.email.data,
             donor_phone_number=form.donor_phone_number.data,
             day_hour=form.day_hour.data).save()
        return redirect(url_for("user_index"))
    print(form.email.data)
    print(form.day_hour.data)
    return render_template("turn/new.html", turn_id=id, form=form)


@login_required
@permission('user_update')
def edit(id, id_turn):
    turn = Turn.query.get(id_turn)

    if not turn:
        add_alert(Alert("danger", "El turno no existe."))
        return redirect(url_for("user_index"))

    return render_template("turn/edit.html", id_center=id, id_turn=id_turn, form=TurnForm(obj=turn))


@login_required
@permission('user_update')
def update(id, id_turn):
    form = TurnForm()

    if not form.validate_on_submit():
        return render_template("turn/edit.html", id_center=id, id_turn=id_turn, form=form)

    turn = Turn.update(id_turn, id, form.email.data,
                       form.donor_phone_number.data, form.day_hour.data)

    if not form:
        add_alert(Alert("danger", "El turno no existe."))
        return redirect(url_for("user_index"))

    add_alert(
        Alert("success", f"El turno de {turn.email} se actualizo correctamente."))

    return redirect(url_for("user_index"))


@login_required
@permission('user_delete')
def delete(id, id_turn):
    center = HelpCenter.query.get(id)
    if not center:
        add_alert(Alert("danger", "El centro no existe."))
        return redirect(url_for("user_index"))

    if center.has_turn(Turn.query.get(id_turn)):
        turn = Turn.delete(id_turn)
        add_alert(
            Alert("success", f"El turno de {turn.email} se borro con exito."))
    else:
        add_alert(Alert("danger", "El turno no existe."))

    return redirect(url_for("user_index"))
