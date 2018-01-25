from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField("usuário", validators=[DataRequired()])
    password = PasswordField("senha", validators=[DataRequired()])
    remember_me = BooleanField("lembrar de mim")
    submit = SubmitField("entrar")
