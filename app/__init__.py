from os import path, environ
from flask import Flask, g
from config.config import config
from .db import set_db, delete_db
from config.routes import set_routes
from app.helpers.login import set_login, authenticated

def create_app(environment="development" ):

    # Configuración inicial de la app
    app = Flask(__name__)
    
    # Carga de la configuración
    env = environ.get("FLASK_ENV", "development")

    app.config.from_object(config[env])

    # Añade a la app flask login
    set_login(app)

    # Establece la db que posee la app
    set_db(app)
   
    # Funciones que se exportan al contexto de Jinja2
    app.jinja_env.globals.update(is_authenticated=authenticated)

    # Establece las rutas que posee la app
    set_routes(app)
 
    # Retornar la instancia de app configurada
    return app

def delete_app(app):
    delete_db(app)