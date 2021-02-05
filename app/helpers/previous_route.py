from flask import session


def add_route(route, name="previus"):
    session[name] = route


def get_route(name="previus"):
    route = session.get(name, None)
    if route:
        session.pop(name)
    return route
