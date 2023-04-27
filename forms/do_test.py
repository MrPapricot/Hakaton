from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField, RadioField
from wtforms.validators import DataRequired


class DoTestForm(FlaskForm):
    submit = SubmitField('Завершить')
    tasks = []

    def __init__(self, tasks):
        self.tasks.clear()
        for i in tasks:
            task =[i['question'], [str(j) for j in i['variants']], i['answers']]
            self.tasks.append(task)
        super().__init__()


