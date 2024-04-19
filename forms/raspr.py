from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired


class RasprForm(FlaskForm):
    style = {'class': 'form-control', 'style': 'border-radius: 25px; margin-left: 10px;  width: 90%; padding-right: 10px;'}
    style_btn = {
        'style': 'border-radius: 5px;  width: auto; font-size: 18px; padding: 5px; margin: 0; margin-right: 23px;'}
    raspr_dot_count = StringField("Количество точек", validators=[DataRequired()], render_kw=style)
    dropdown_list = ['равномерное', 'треугольное',
                     'бета', 'экспоненциальное', 'гамма', 'нормальное', 'логнормальное', 'парето']
    raspr_name = SelectField('Распределение', choices=dropdown_list, default=1, render_kw=style)
    submit = SubmitField('Построить график', render_kw=style_btn)
