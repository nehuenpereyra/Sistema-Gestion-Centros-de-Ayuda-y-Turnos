from flask import render_template
from app.helpers import handler
from app.resources import user
from app.resources import auth
from app.resources import configuration
from app.helpers.login import authenticated
from flask import redirect, url_for


def set_routes(app):

    # Ruta para el Home (usando decorator)
    @app.route("/")
    def index():
        if authenticated() == True:
            return render_template("home.html")
        else:
            return redirect(url_for("auth_login"))

    # Autenticación
    app.add_url_rule("/iniciar_sesion", "auth_login", auth.login)
    app.add_url_rule("/cerrar_sesion", "auth_logout", auth.logout)
    app.add_url_rule(
        "/autenticacion", "auth_authenticate", auth.authenticate, methods=["POST"]
    )

    # Rutas de Usuarios
    app.add_url_rule("/usuarios", "user_index", user.index)
    app.add_url_rule("/usuarios", "user_create", user.create, methods=["POST"])
    app.add_url_rule("/usuarios/nuevo", "user_new", user.new)
    app.add_url_rule("/usuarios/borrar/<int:id>", "user_delete", user.delete)

    # Rutas de Configuracion
    app.add_url_rule("/configuracion", "configuration_update",
                     configuration.update, methods=["POST"])
    app.add_url_rule("/configuracion/editar",
                     "configuration_edit", configuration.edit)

    # Handlers
    app.register_error_handler(404, handler.not_found_error)
    app.register_error_handler(405, handler.not_found_error)
    app.register_error_handler(401, handler.unauthorized_error)
    app.register_error_handler(403, handler.forbidden_error)
    # Implementar lo mismo para el error 500 y 401
