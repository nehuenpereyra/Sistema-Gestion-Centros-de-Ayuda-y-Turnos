from flask import redirect, render_template, request, url_for, abort
from app.models.user import User
from app.helpers.forms.SignupForm import SignupForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required

# Protected resources


@login_required
def index():
    users = User.all()
    return render_template("user/index.html", users=users)


@login_required
def new():
    return render_template("user/new.html", form=SignupForm())


@login_required
def create():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data,
                    first_name=form.first_name.data, last_name=form.last_name.data,
                    password=generate_password_hash(form.password.data))
        user.save()
        login_user(user, remember=True)  # Dejamos al usuario logueado
        return redirect(url_for("user_index"))

    return render_template("user/new.html", form=form)


@login_required
def delete(id):
    user = User.get_by_id(id)
    if user:
        user.delete()
    return redirect(url_for("user_index"))
