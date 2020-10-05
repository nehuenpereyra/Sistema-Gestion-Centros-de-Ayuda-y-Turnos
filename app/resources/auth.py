from flask import redirect, render_template, request, url_for, abort, flash
from app.models.user import User
from app.helpers.forms.LoginForm import LoginForm
from flask_login import login_user, logout_user

def login():
    return render_template("auth/login.html", form=LoginForm())


def authenticate():
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.find_by_email(form.email.data)
        if (user is not None) and (user.check_password(form.password.data)):
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for("home")) 
    #return redirect(url_for("auth_login"))
    return render_template("auth/login.html", form=form, authError=True)


def logout():
    logout_user()
    #flash("La sesión se cerró correctamente.")
    return redirect(url_for("home"))
