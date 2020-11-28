
from flask import request, json, Response, abort

from app.models.configuration import Configuration
from app.models.help_center_type import HelpCenterType


def index():
    page = int(request.args.get("pagina", 1))

    if page < 1:
        abort(400)

    per_page = Configuration.get().pagination_elements
    help_center_types, total = HelpCenterType.all_paginated(
        page=page, per_page=per_page)

    help_center_type_schema = {
        "datos": help_center_types.collect(lambda each: each.public_dict()),
        "pagina": page,
        "por_pagina": per_page,
        "total": total
    }

    return json.jsonify(**help_center_type_schema)
