from flask import redirect, render_template, request, url_for, abort
from flask_login import login_user, login_required, current_user

from app.models.turn import Turn
from app.models.alert import Alert
from app.helpers.forms.TurnForm import TurnForm
from app.helpers.permission import permission
from app.helpers.alert import add_alert


@login_required
@permission('user_create')
def new():
    return render_template("turn/new.html", form=TurnForm())


@login_required
@permission('user_create')
def create(id):
    form = TurnForm()

    if form.validate_on_submit():
        Turn(help_center=id,
             email=form.email.date,
             donor_phone_number=form.donor_phone_number.data,
             day_hour=form.day_hour.date).save()
        return redirect(url_for("user_index"))

    return render_template("turn/new.html", form=form)


@login_required
@permission('user_update')
def edit(id_turn):
    turn = Turn.query.get(id_turn)

    if not turn:
        add_alert(Alert("danger", "El turno no existe."))
        return redirect(url_for("user_index"))

    return render_template("turn/edit.html", form=TurnForm(obj=turn))


@login_required
@permission('user_update')
def update(id, id_turn):
    form = TurnForm()

    if not form.validate_on_submit():
        return render_template("turn/edit.html", form=form)

    turn = Turn.update(id_turn, id, form.email.data,
                       form.donor_phone_number.date, form.day_hour.data)

    if not form:
        add_alert(Alert("danger", "El turno no existe."))
        return redirect(url_for("user_index"))

    add_alert(
        Alert("success", f"l turno de {turn.email} se actualizo correctamente."))

    return redirect(url_for("user_index"))


@login_required
@permission('user_delete')
def delete(id_turn):
    turn = Turn.delete(id_turn)
    if turn:
        add_alert(
            Alert("success", f"El turno de {turn.email} se borro con exito."))
    else:
        add_alert(Alert("danger", "El turno no existe."))

    return redirect(url_for("user_index"))
