from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, IntegerField
from wtforms.validators import DataRequired


class UravnForm(FlaskForm):
    style = {'class': 'form-control', 'style': 'border-radius: 25px; width: 50%; margin-top: 15px;'}
    style_btn = {'style': 'border-radius: 5px;  width: 15%; font-size: 18px; padding: 5px;'}
    uravns = StringField('Введите математическую задачу:', validators=[DataRequired()], render_kw=style)
    submit = SubmitField('Решить', render_kw=style_btn)