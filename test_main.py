from flask import Flask
from data import db_session
from data.task import Tasks
from data.mentor import Mentor
from data.student import Student

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

db_session.global_init("db/test_db.db")
sess = db_session.create_session()
task = sess.query(Tasks).first()
stud = sess.query(Student).first()
stud.tasks.append(task)
sess.commit()
for i in sess.query(Student):
    print(i.name)
    print(i.tasks)
    print('\n')