from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class MainForm(FlaskForm):
    function = StringField("Функция")
    submit = SubmitField('Построить график')
