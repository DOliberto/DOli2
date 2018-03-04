REGULAR_FORM_TEMPLATE = """from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

{% for form in forms %}

class {{ form.name|capitalize|trim }}(FlaskForm):
    {% for field in form.fields %}{{ field.var_name }} = {{ field.type|capitalize|trim }}({{ field.label}}, validators=[{{ field.validators|join(', ') }}])
    {% endfor %}submit = SubmitField("Submeter")

{% endfor %}
"""
