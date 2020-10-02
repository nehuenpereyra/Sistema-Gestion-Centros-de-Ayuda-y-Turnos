from flask import redirect, render_template, request, url_for, session, abort
from app.models.user import User
from app.helpers.auth import authenticated

# Protected resources
def index():
    if not authenticated(session):
        abort(401)

    users = User.all()
#<li>{{ user.email }} - {{ user.first_name }} - {{ user.last_name }} - {{ user.password }}</li>
    return render_template("user/index.html", users=users)


def new():
    if not authenticated(session):
        abort(401)

    return render_template("user/new.html")


def create():
    if not authenticated(session):
        abort(401)

    User(email=request.form["email"], first_name=request.form["first_name"],
    last_name=request.form["last_name"],password=request.form["password"]).save()
    #conn = connection()
    #User.create(conn, request.form)
    return redirect(url_for("user_index"))
