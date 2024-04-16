from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class RasprForm(FlaskForm):
    raspr_dot_count = StringField("Количество точек", validators=[DataRequired()])
