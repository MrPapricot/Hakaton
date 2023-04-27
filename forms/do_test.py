from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField, RadioField, FieldList
from wtforms.validators import DataRequired


class DoTestForm(FlaskForm):
    submit = SubmitField('Завершить')
    list = FieldList(RadioField('Вопрос', choices=['1', '2', '3']))

    def __init__(self, tasks):
        super().__init__()
        self.list = FieldList(RadioField('Вопрос', choices=['1', '2', '3']))
        for i in tasks:
            task = RadioField(i['question'], choices=[str(j) for j in i['variants']])
            self.list.append_entry(task)


