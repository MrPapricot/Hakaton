from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class TestForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField("Дополнительная информация")
    students = StringField('ID учеников через запятую (1, 2, 3, ...)', validators=[DataRequired()])
    file = FileField('Теоретический материал', validators=[FileAllowed(['html'], 'Только файлы html')])
    submit = SubmitField('Применить')