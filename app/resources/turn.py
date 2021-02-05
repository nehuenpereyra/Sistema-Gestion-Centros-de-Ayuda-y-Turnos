from datetime import date, timedelta, datetime
from flask import redirect, render_template, request, url_for, abort, Response, jsonify
from flask_login import login_user, login_required, current_user
from flask import abort

from app.models.turn import Turn
from app.models.alert import Alert
from app.models.configuration import Configuration
from app.models.help_center import HelpCenter
from app.helpers.forms.TurnForm import TurnForm
from app.helpers.permission import permission
from app.helpers.alert import add_alert, get_alert
from app.helpers.previous_route import add_route, get_route
from app.helpers.forms.TurnSeekerForm import TurnSeekerForm
import json


@login_required
@permission('turn_index')
def index():
    search_form = TurnSeekerForm(request.args)
    turns = Turn.get_next_tuns(search_query=search_form.search_query.data,
                               email=search_form.email.data,
                               page=int(request.args.get('page', 1)),
                               per_page=Configuration.query.first().pagination_elements)
    add_route(url_for("turn_index"))
    return render_template("turn/index.html", turns=turns, alert=get_alert(), search_form=search_form)


@login_required
@permission('turn_index')
def center_index(id):
    search_form = TurnSeekerForm(request.args)
    center = HelpCenter.query.get(id)
    if not center:
        add_alert(Alert("danger", "El centro no existe."))
        return redirect(url_for("help_center_index"))

    if center.is_in_pending_state():
        add_alert(Alert(
            "danger", "No se puede acceder ya que el centro esta pendiente de aceptación."))
        return redirect(url_for("help_center_index"))

    if center.is_in_rejected_state():
        add_alert(
            Alert("danger", "No se puede acceder ya que el centro esta rechazado."))
        return redirect(url_for("help_center_index"))

    turns = Turn.search(id_center=id, email=search_form.email.data, page=int(request.args.get('page', 1)),
                        per_page=Configuration.query.first().pagination_elements)

    add_route(url_for("turn_center_index", id=id))
    return render_template("turn/center_index.html", id_center=id, turns=turns, alert=get_alert(), center=center, search_form=search_form, today=datetime.today())


@login_required
@permission('turn_create')
def new(id):
    center = HelpCenter.query.get(id)
    if not center:
        add_alert(Alert("danger", "El centro no existe."))
        return redirect(url_for("turn_center_index", id=id))
    return render_template("turn/new.html", center_id=id, form=TurnForm(), center=center)


@login_required
@permission('turn_create')
def create(id):

    center = HelpCenter.query.get(id)
    if not center:
        add_alert(Alert("danger", "El centro no existe."))
        return redirect(url_for("turn_center_index", id=id))

    form = TurnForm(center_id=id, id=None)

    if form.validate_on_submit():
        turn = Turn(help_center=center,
                    email=form.email.data,
                    donor_phone_number=form.donor_phone_number.data,
                    day_hour=datetime.combine(form.date_turn.data, form.time_turn.data))
        turn.save()
        add_alert(
            Alert("success", f"El turno con fecha {turn.day_hour.strftime('%Y/%m/%d-%H:%M:%S')} de {turn.email} se creo correctamente."))
        return redirect(url_for("turn_center_index", id=id))

    return render_template("turn/new.html", center_id=id, form=form, center=center)


@login_required
@permission('turn_update')
def edit(id, id_turn):
    turn = Turn.query.get(id_turn)
    center = HelpCenter.query.get(id)

    if not center:
        add_alert(Alert("danger", "El centro no existe."))
        return redirect(url_for("help_center_index"))

    if not turn:
        add_alert(Alert("danger", "El turno no existe."))
        return redirect(url_for("turn_center_index", id=id))

    if not center.turns.any_satisfy(lambda each: each.id == turn.id):
        add_alert(Alert("danger", "El centro no tiene ese turno asignado."))
        return redirect(url_for("turn_center_index", id=id))

    form = TurnForm(obj=turn)
    form.date_turn.data = turn.day_hour.date()
    form.time_turn.data = turn.day_hour.time()
    return render_template("turn/edit.html", id_center=id, id_turn=id_turn, form=form, center=center)


@login_required
@permission('turn_update')
def update(id, id_turn):
    form = TurnForm(id=id_turn, center_id=id)

    if not form.validate_on_submit():
        return render_template("turn/edit.html", id_center=id, id_turn=id_turn, form=form, center=HelpCenter.query.get(id))

    turn = Turn.update(id_turn, id, form.email.data,
                       form.donor_phone_number.data, datetime.combine(form.date_turn.data, form.time_turn.data))

    if not form:
        add_alert(Alert("danger", "El turno no existe."))
        return redirect(url_for("turn_center_index", id=id))

    add_alert(
        Alert("success", f"El turno de {turn.email} se actualizo correctamente."))

    return redirect(get_route())


@login_required
@permission('turn_delete')
def delete(id, id_turn):
    center = HelpCenter.query.get(id)
    if not center:
        add_alert(Alert("danger", "El centro no existe."))
        return redirect(url_for("turn_center_index", id=id))

    turn = Turn.query.get(id_turn)
    if center.has_turn(turn):
        if turn.day_hour < datetime.today():
            add_alert(Alert(
                "danger", "El turno no se puede eliminar, posee una fecha anterior a la actual."))
            return redirect(url_for("turn_center_index", id=id))
        turn = Turn.delete(id_turn)
        add_alert(
            Alert("success", f"El turno de {turn.email} se borro con exito."))
    else:
        add_alert(Alert("danger", "El turno no existe."))

    return redirect(url_for("turn_center_index", id=id))
