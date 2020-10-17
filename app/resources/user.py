from werkzeug.security import generate_password_hash, check_password_hash

from flask import redirect, render_template, request, url_for, abort
from flask_login import login_user, login_required

from app.helpers.forms.SignupForm import SignupForm
from app.helpers.forms.UserSeekerForm import UserSeekerForm
from app.helpers.permission import permission
from app.models.user import User
from app.models.configuration import Configuration


@login_required
@permission('user_index')
def index(state=None, notification_state=None):

    search_form = UserSeekerForm(request.args)
    query = User.query

    if (search_form.data_seeker.data or search_form.user_state.data):

        if (search_form.data_seeker.data):
            query = query.filter_by(username=search_form.data_seeker.data)

        if (search_form.user_state.data):
            active_user = search_form.user_state.data == "active"
            query = query.filter_by(is_active=active_user)

    page = int(request.args.get('page', 1))
    per_page = Configuration.query.first().pagination_elements

    users = query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template("user/index.html", users=users, search_form=search_form, state=state, notification_state=notification_state)


@login_required
@permission('user_create')
def new():
    return render_template("user/new.html", form=SignupForm())


@login_required
@permission('user_update')
def edit(id):
    user = User.query.get(id)

    if not user:
        return redirect(url_for("user_index"))

    return render_template("user/edit.html", user_id=id, update_form=UpdateUserForm(obj=user))


@login_required
@permission('user_update')
def update(id):
    update_form = UpdateUserForm()

    if not update_form.validate_on_submit():
        return render_template("user/edit.html", user_id=id, update_form=update_form)

    user = User.query.get(id)

    if not user:
        # luego, se deberia mostrar un mensaje de error
        return redirect(url_for("index"))

    user.name = update_form.name.data
    user.surname = update_form.surname.data
    user.email = update_form.email.data
    user.username = update_form.username.data
    user.roles = update_form.roles.data
    user.is_active = update_form.is_active.data

    if update_form.password.data:
        user.set_password(update_form.password.data)

    user.save()

    return redirect(url_for("user_index"))


@login_required
@permission('user_create')
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
@permission('user_delete')
def delete(id):
    user = User.get_by_id(id)
    if user:
        user.delete()
    return redirect(url_for("user_index", state="success", notification_state=f"El usuario {user.username} fue eliminado con exito"))
