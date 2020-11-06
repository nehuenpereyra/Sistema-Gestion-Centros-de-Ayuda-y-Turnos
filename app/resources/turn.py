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

import json


@login_required
@permission('turn_index')
def index():

    turns = Turn.get_next_tuns(page=int(request.args.get('page', 1)),
                               per_page=Configuration.query.first().pagination_elements)

    if turns.items.size() == 0:
        add_alert(Alert("danger", "No tiene turnos cargados."))

    return render_template("turn/index.html", turns=turns, alert=get_alert())


@login_required
@permission('turn_index')
def center_index(id):

    turns = Turn.search(id_center=id, page=int(request.args.get('page', 1)),
                        per_page=Configuration.query.first().pagination_elements)

    if turns.items.size() == 0:
        add_alert(Alert("danger", "No tiene turnos cargados."))

    return render_template("turn/center_index.html", id_center=id, turns=turns, alert=get_alert())


@login_required
@permission('turn_create')
def new(id):
    return render_template("turn/new.html", center_id=id, form=TurnForm())


@login_required
@permission('turn_create')
def create(id):
    form = TurnForm()

    center = HelpCenter.query.get(id)
    if not center:
        add_alert(Alert("danger", "El centro no existe."))
        return redirect(url_for("turn_center_index", id=id))

    if form.validate_on_submit():
        Turn(help_center=HelpCenter.query.get(id),
             email=form.email.data,
             donor_phone_number=form.donor_phone_number.data,
             day_hour=form.day_hour.data).save()
        return redirect(url_for("turn_center_index", id=id))
    print(form.email.data)
    print(form.day_hour.data)
    return render_template("turn/new.html", center_id=id, form=form)


@login_required
@permission('turn_update')
def edit(id, id_turn):
    turn = Turn.query.get(id_turn)

    if not turn:
        add_alert(Alert("danger", "El turno no existe."))
        return redirect(url_for("turn_center_index", id=id))

    return render_template("turn/edit.html", id_center=id, id_turn=id_turn, form=TurnForm(obj=turn))


@login_required
@permission('turn_update')
def update(id, id_turn):
    form = TurnForm()

    if not form.validate_on_submit():
        return render_template("turn/edit.html", id_center=id, id_turn=id_turn, form=form)

    turn = Turn.update(id_turn, id, form.email.data,
                       form.donor_phone_number.data, form.day_hour.data)

    if not form:
        add_alert(Alert("danger", "El turno no existe."))
        return redirect(url_for("turn_center_index", id=id))

    add_alert(
        Alert("success", f"El turno de {turn.email} se actualizo correctamente."))

    return redirect(url_for("turn_center_index", id=id))


@login_required
@permission('turn_delete')
def delete(id, id_turn):
    center = HelpCenter.query.get(id)
    if not center:
        add_alert(Alert("danger", "El centro no existe."))
        return redirect(url_for("turn_center_index", id=id))

    if center.has_turn(Turn.query.get(id_turn)):
        turn = Turn.delete(id_turn)
        add_alert(
            Alert("success", f"El turno de {turn.email} se borro con exito."))
    else:
        add_alert(Alert("danger", "El turno no existe."))

    return redirect(url_for("turn_center_index", id=id))


def free_time(id):

    center = HelpCenter.query.get(id)
    if not center:
        abort(400)

    search_date = date.today()
    if request.args.get('fecha'):
        try:
            search_date = datetime.strptime(
                request.args.get('fecha'), '%Y-%m-%d').date()
        except ValueError:
            abort(500)

    return Response(response=Turn.all_free_time_json(id, search_date), status=200, mimetype="application/json")


def reserved(id):
    form_ok = {
        "center_id": "1",
        "email": "tito@gmail.com",
        "donor_phone_number": "4093184",
        "day_hour": str(datetime(2020, 11, 5).strftime("%Y/%m/%d, %H:%M:%S"))}
    #form_okk = jsonify(form_ok)
    print(form_ok)
    # jsonify(request.json)
    form_okkk = json.dumps(form_ok)
    form = TurnForm(obj=form_okkk)
    if form.validate():
        print("El fomulario es Correcto")
    else:
        print("El fomulario es Incorrecto")
    #    abort(500)
    for fieldName, errorMessages in form.errors.items():
        print(fieldName)
        for err in errorMessages:
            print(err)

    return Response(response=json.dumps(form_ok), status=200, mimetype="application/json")
