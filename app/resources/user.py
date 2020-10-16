from flask import redirect, render_template, request, url_for, abort
from app.models.user import User
from app.helpers.forms.SignupForm import SignupForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required
from app.helpers.forms.UserSeekerForm import UserSeekerForm

# Protected resources


@login_required
def index(state=None, notification_state=None):

    search_form = UserSeekerForm(request.args)
    query = User.query

    if (search_form.data_seeker.data or search_form.user_state.data):

        if (search_form.data_seeker.data):
            query = query.filter_by(username=search_form.data_seeker.data)

        if (search_form.user_state.data):
            if search_form.user_state.data == "active":
                query = query.filter_by(is_active=True)
            else:
                query = query.filter_by(is_active=False)

    users = query.all()

    return render_template("user/index.html", users=users, search_form=search_form, state=state, notification_state=notification_state)


@login_required
def new():
    return render_template("user/new.html", form=SignupForm())


@login_required
def create():
    form = SignupForm()
    if form.validate_on_submit():
        User(username=form.username.data, email=form.email.data,
             name=form.name.data, surname=form.surname.data,
             password=generate_password_hash(form.password.data),
             roles=form.roles.data).save()
        return redirect(url_for("user_index"))

    return render_template("user/new.html", form=form)


@login_required
def delete(id):
    user = User.get_by_id(id)
    if user:
        user.delete()
    return redirect(url_for("user_index", state="success", notification_state=f"El usuario {user.username} fue eliminado con exito"))
