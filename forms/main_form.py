from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, ValidationError


class MainForm(FlaskForm):
    style = {'class': 'form-control', 'style': 'border-radius: 25px; margin-left: 10px;  width: 90%;'}
    style_btn = {'style': "margin-top: 5px; color: #fff; border-color: teal; background-color: teal;"}
    function = StringField("Функция", validators=[DataRequired()], render_kw=style)
    start_dot = IntegerField('Начальная координата', validators=[DataRequired()], render_kw=style)
    end_dot = IntegerField('Конечная координата', validators=[DataRequired()], render_kw=style)
    count = IntegerField('Количество точек', validators=[DataRequired()], render_kw=style)
    submit = SubmitField('Построить график')
