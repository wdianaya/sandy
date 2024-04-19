from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, FileField, SelectField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    style = {'class': 'form-control', 'style': 'border-radius: 10px; margin-left: 10px;  margin-right: 10px;'}
    style_btn = {
        'style': 'border-radius: 5px;  width: auto; font-size: 18px; padding: 5px; margin: 0; margin-right: 23px;'}
    title = StringField('Заголовок', validators=[DataRequired()], render_kw=style)
    content = TextAreaField('Статья', validators=[DataRequired()], render_kw=style)
    picture = FileField('Изображение (png, jpg)', validators=[FileAllowed(['jpg', 'png'])], render_kw=style)
    submit = SubmitField('Опубликовать', render_kw=style_btn)

class Comment(FlaskForm):
    text = StringField('Ваш комментарий', validators=[DataRequired()])
    submit = SubmitField('Опубликовать')