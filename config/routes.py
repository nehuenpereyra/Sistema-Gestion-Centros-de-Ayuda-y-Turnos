from flask import render_template
from flask import redirect, url_for
from flask_login import current_user

from app.resources import user
from app.resources import auth
from app.resources import configuration
from app.helpers import handler
from app.helpers.login import authenticated


def set_routes(app):
    """Configure application paths

    Keyword arguments:
    app -- application to which the routes will be added
    """

    # Ruta para el Home (usando decorator)
    @app.route("/")
    def index():
        if authenticated() == True:
            if current_user.roles[0].name == "Administrador":
                return redirect(url_for("user_index"))
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
    app.add_url_rule("/usuario/perfil", "user_profile", user.profile)
    app.add_url_rule("/usuarios/", "user_index", user.index)

    app.add_url_rule("/usuario/nuevo", "user_new", user.new)
    app.add_url_rule("/usuario/nuevo", "user_create",
                     user.create, methods=["POST"])

    app.add_url_rule("/usuario/editar/<int:id>", "user_edit", user.edit)
    app.add_url_rule("/usuario/actualizar/<int:id>", "user_update", user.update,
                     methods=["POST"])

    app.add_url_rule("/usuario/borrar/<int:id>", "user_delete", user.delete)

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
