from flask import redirect, render_template, url_for
from flask_login import login_user, logout_user
# from flask_login import current_user

from app.models.user import User
from app.helpers.forms.LoginForm import LoginForm
from app.helpers.login import authenticated
from app.helpers.oauth import get_oauth


def login():
    if authenticated() == True:
        return redirect(url_for("index"))
    return render_template("auth/login.html", form=LoginForm())

def login_google():
    oauth = get_oauth()
    google = oauth.create_client('google')
    return google.authorize_redirect(url_for("auth_google", _external=True))

def authorize_google():
    oauth = get_oauth()
    token = oauth.google.authorize_access_token()
    user = User.find_by_email(oauth.google.userinfo().email)
    if (user is not None):
        login_user(user, remember=user.id)
        return redirect(url_for("index"))
    return render_template("auth/login.html", form=LoginForm(), authError=True)

def authenticate():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.find_by_email(form.email.data)
        if (user is not None) and (user.check_password(form.password.data)):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for("index"))
    return render_template("auth/login.html", form=form, authError=True)


def logout():
    logout_user()
    return redirect(url_for("index"))
