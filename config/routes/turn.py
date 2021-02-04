from app.resources import turn
import app.resources.api.turn as api_turn


def set_routes(app):
    # Rutas de Turno
    app.add_url_rule("/turnos", "turn_index", turn.index)
    app.add_url_rule("/centro/<int:id>/turnos",
                     "turn_center_index", turn.center_index)
    app.add_url_rule("/centro/<int:id>/turno/nuevo", "turn_new", turn.new)
    app.add_url_rule("/centro/<int:id>/turno/nuevo", "turn_create",
                     turn.create, methods=["POST"])
    app.add_url_rule(
        "/centro/<int:id>/turno/actualizar/<int:id_turn>", "turn_edit", turn.edit)
    app.add_url_rule("/centro/<int:id>/turno/actualizar/<int:id_turn>", "turn_update", turn.update,
                     methods=["POST"])
    app.add_url_rule("/centro/<int:id>/turno/borrar/<int:id_turn>",
                     "turn_delete", turn.delete)

    # Rutas de la API de turnos
    app.add_url_rule(
        "/api/centros/<int:id>/turnos_disponibles/", "turn_free_time", api_turn.free_time)
    app.add_url_rule(
        "/api/cantidad_turnos/", "turn_quantity_turns_last", api_turn.quantity_turns_last)
    app.add_url_rule("/api/centros/<int:id>/reserva",
                     "turn_reserved", api_turn.reserved, methods=["POST"])
