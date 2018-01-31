from app.models import User

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    username = StringField("usuário", validators=[DataRequired()])
    password = PasswordField("senha", validators=[DataRequired()])
    remember_me = BooleanField("lembrar de mim")
    submit = SubmitField("entrar")

class RegistrationForm(FlaskForm):
    username = StringField("usuário", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired(), Email()])
    #entity = StringField("entidade governamental", validators=[DataRequired()])
    #subentity = StringField("sub-entidade governamental", validators=[DataRequired()])
    password = PasswordField("senha", validators=[DataRequired()])
    password2 = PasswordField(
        "repita a senha", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("registrar")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("usuário já existe, escolha outro.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("este e-mail já foi cadastrado, por favor escolha outro.")
