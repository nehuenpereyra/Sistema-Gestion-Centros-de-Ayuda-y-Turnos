from app.resources import main


def set_routes(app):
    app.add_url_rule("/", "main_index", main.index)
