from os import path, environ
from flask import Flask, g
from flask_session import Session
from config.config import config
from .db import set_db
from config.routes import set_routes
from app.helpers.login import set_login, authenticated
from app.helpers.permission import verify_permission


def create_app(environment="development"):

    # Configuración inicial de la app
    app = Flask(__name__)

    # Agrega el manejo se seciones
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # Carga de la configuración
    env = environ.get("FLASK_ENV", "development")
    app.config.from_object(config[env])

    # Añade a la app flask login
    set_login(app)

    # Establece la db que posee la app
    set_db(app)

    # Funciones que se exportan al contexto de Jinja2
    app.jinja_env.globals.update(is_authenticated=authenticated)
    app.jinja_env.globals.update(verify_permission=verify_permission)

    # Establece las rutas que posee la app
    set_routes(app)

    # Retornar la instancia de app configurada
    return app
