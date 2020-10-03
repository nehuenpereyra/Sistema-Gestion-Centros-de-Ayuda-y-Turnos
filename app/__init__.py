from os import path, environ
from flask import Flask, g
from flask_session import Session
from config.config import config
from .db import set_db
from config.routes import set_routes
from app.helpers import auth as helper_auth

def create_app(environment="development"):
    # Configuración inicial de la app
    app = Flask(__name__)

    # Carga de la configuración
    env = environ.get("FLASK_ENV", environment)
    app.config.from_object(config[env])

    # Server Side session
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # Establece la db que posee la app
    set_db(app)
   
    # Funciones que se exportan al contexto de Jinja2
    app.jinja_env.globals.update(is_authenticated=helper_auth.authenticated)

    # Establece las rutas que posee la app
    set_routes(app)
 
    # Retornar la instancia de app configurada
    return app
