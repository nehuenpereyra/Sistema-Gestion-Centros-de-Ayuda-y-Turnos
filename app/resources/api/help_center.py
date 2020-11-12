
from datetime import time

from flask import request, json, Response, abort

from app.helpers.forms.HelpCenterApiForm import HelpCenterApiForm
from app.models.configuration import Configuration
from app.models.help_center import HelpCenter
from app.models.help_center_type import HelpCenterType
from app.models.town import Town


def default_json(default=str):
    def function(input):
        if isinstance(input, time):
            return input.strftime("%H:%M")
        else:
            return default
    return function


def index():
    page = int(request.args.get("pagina", 1))

    if page < 1:
        abort(400)

    per_page = Configuration.get().pagination_elements
    help_centers, total = HelpCenter.all_published(
        page=page, per_page=per_page)

    help_center_schema = {
        "centros": help_centers.collect(lambda each: each.public_dict()),
        "pagina": page,
        "por_pagina": per_page,
        "total": total
    }

    return json.jsonify(**help_center_schema)


def show(id):

    help_center = HelpCenter.get_public_center(id)

    if not help_center:
        abort(404)

    help_center_schema = {
        "atributos": help_center.public_dict()
    }

    return json.jsonify(**help_center_schema)


def create():

    form = HelpCenterApiForm(obj=request.json, meta={'csrf': False}, id=None)

    if not form.validate_on_submit():
        abort(400)

    HelpCenter(
        name=form.nombre.data,
        address=form.direccion.data,
        phone_number=form.telefono.data,
        opening_time=form.hora_apertura.data,
        closing_time=form.hora_cierre.data,
        center_type=HelpCenterType.get_by_name(form.tipo_centro.data),
        town=Town.get_by_name(form.municipio.data),
        web_url=form.web_url.data,
        email=form.email.data,
        latitude=form.latitud.data,
        longitude=form.longitud.data
    ).save()

    success_schema = {"atributos": {key: value for key, value
                                    in form.data.items() if value is not None}}

    return json.dumps(success_schema, default=default_json()), {"Content-Type": "application/json"}