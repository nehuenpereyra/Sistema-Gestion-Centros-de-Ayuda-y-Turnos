from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectMultipleField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, Length
from app.models.user_role import UserRole
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField


class SignupForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(max=20)])
    surname = StringField('Apellido', validators=[
                          DataRequired(), Length(max=20)])
    username = StringField('Nombre de usuario', validators=[
                           DataRequired(), Length(max=20)])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=6, max=20)])
    email = EmailField('Email', validators=[DataRequired(), Email()])

    roles = QuerySelectMultipleField("Roles", query_factory=lambda: UserRole.query.all(
    ), get_label="name", validators=[DataRequired()])

    submit = SubmitField('Registrar')
