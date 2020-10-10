from flask import abort
from flask_login import current_user

def verify_permission(permission):
    print("Verificacion del permiso")
    return True

def permission(name):
    def wrapper_1(function):
        def wrapper_2(*args, **kwargs):    
            if not verify_permission(name):
                abort(403)
            return function(*args, **kwargs)
        return wrapper_2
    return wrapper_1
