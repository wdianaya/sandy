from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired


class RasprForm(FlaskForm):
    raspr_dot_count = StringField("Количество точек", validators=[DataRequired()])
    dropdown_list = ['равномерное', 'треугольное',
                     'бета', 'экспоненциальное', 'гамма', 'нормальное', 'логнормальное', 'парето']
    raspr_name = SelectField('Распределение', choices=dropdown_list, default=1)
    submit = SubmitField('Построить график')
