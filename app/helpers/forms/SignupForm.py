from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(FlaskForm):
    first_name = StringField('Nombre', validators=[DataRequired(), Length(max=12)])
    last_name = StringField('Apellido', validators=[DataRequired(), Length(max=64)])
    username = StringField('Nombre de usuario', validators=[DataRequired(), Length(max=64)])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Registrar')