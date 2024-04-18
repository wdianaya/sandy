from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, IntegerField
from wtforms.validators import DataRequired


class UravnForm(FlaskForm):
    uravns = StringField('Введите математическую задачу:', validators=[DataRequired()])
    submit = SubmitField('Submit')