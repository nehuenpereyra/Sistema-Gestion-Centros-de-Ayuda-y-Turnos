import os
from flask import json
from authlib.integrations.flask_client import OAuth

oauth = OAuth()

def set_oauth(app):
    SITE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
    json_url_google = os.path.join(SITE_ROOT, "static","oauth", "client_secret_google.json")
    json_data_google = json.load(open(json_url_google))
    
    oauth.init_app(app)
    oauth.register(**json_data_google)
        


def get_oauth():
    return oauth