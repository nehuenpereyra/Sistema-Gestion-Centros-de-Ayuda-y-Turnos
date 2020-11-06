
from flask import request, json, abort

from app.models.configuration import Configuration
from app.models.help_center import HelpCenter


def index():
    page = int(request.args.get("pagina", 1))

    if page < 1:
        abort(500)

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
