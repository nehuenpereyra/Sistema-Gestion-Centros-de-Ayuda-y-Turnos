from app.resources import auth


def set_routes(app):
    # Autenticación
    app.add_url_rule("/iniciar_sesion", "auth_login", auth.login)
    app.add_url_rule("/cerrar_sesion", "auth_logout", auth.logout)
    app.add_url_rule(
        "/autenticacion", "auth_authenticate", auth.authenticate, methods=["POST"]
    )
    app.add_url_rule("/login/google", "login_google", auth.login_google)
    app.add_url_rule("/autorizar/google", "auth_google", auth.authorize_google)
