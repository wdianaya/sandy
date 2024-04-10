from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class MainForm(FlaskForm):
    function = StringField("Функция", validators=[DataRequired()])
    start_dot = IntegerField('Начальная координата', validators=[DataRequired()])
    end_dot = IntegerField('Конечная координата', validators=[DataRequired()])
    count = IntegerField('Количество точек', validators=[DataRequired()])
    submit = SubmitField('Построить график')
