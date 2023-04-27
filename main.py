import json

from flask import Flask, redirect, render_template, request
from data import db_session
from flask import Flask
from data import db_session
from data.task import Tasks
from data.student import Student
from data.relationships import Relationship
from flask_login import LoginManager, login_user, login_required, current_user
from forms.register import RegisterForm
from forms.login import LoginForm
from forms.test import TestForm
from forms.theory import TheoryForm
from tinydb import TinyDB, Query
from forms.do_theory import DoTheoryForm
from forms.do_test import DoTestForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/database.db")
results = TinyDB('results.json')
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(student_id):
    db_sess = db_session.create_session()
    return db_sess.query(Student).get(student_id)


def main():
    app.run(debug=True)


def add_task(*, task, students: list):
    sess = db_session.create_session()
    for i in students:
        rel = Relationship()
        rel.student_id = i.id
        rel.task_id = task.id
        sess.add(rel)
    sess.commit()


def get_tasks(student):
    sess = db_session.create_session()
    tasks = []
    for i in sess.query(Relationship).filter(Relationship.student_id == student.id).all():
        tasks.append(sess.query(Tasks).filter(Tasks.id == i.task_id).first())
    return tasks


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(Student).filter(Student.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/tasks/')
@login_required
def tasks():
    return render_template('tasks.html', task_list=get_tasks(current_user))


@app.route('/add_test/', methods=['GET', 'POST'])
@login_required
def add_test():
    if current_user.is_mentor:
        form = TestForm()
        if form.validate_on_submit():
            sess = db_session.create_session()
            task = Tasks()
            task.test = True
            task.title = form.title.data
            task.deadline = form.deadline.data
            file = form.file.data
            file.save('tasks/' + file.filename)
            task.path = 'tasks/' + file.filename
            if form.students.data == '@all':
                students = sess.query(Student).all()
            else:
                students = [sess.query(Student).filter(Student.id == i).first() for i in form.students.data.split(', ')]
            sess.add(task)
            sess.commit()
            add_task(task=task, students=students)
            return redirect('/')
        return render_template('task.html', form=form)


@app.route('/add_theory/', methods=['GET', 'POST'])
@login_required
def add_theory():
    if current_user.is_mentor:
        form = TestForm()
        if form.validate_on_submit():
            sess = db_session.create_session()
            task = Tasks()
            task.test = False
            task.title = form.title
            task.deadline = form.deadline
            file = form.file.data
            file.save('tasks/' + file.filename)
            task.path = 'tasks/' + file.filename
            if form.students.data == '@all':
                students = sess.query(Student).all()
            else:
                students = [sess.query(Student).filter(Student.id == i).first() for i in form.students.data.split(', ')]
            sess.add(task)
            sess.commit()
            add_task(task=task, students=students)
            return redirect('/')
        return render_template('task.html', form=form)


@app.route('/do_task/<int:id>/', methods=['GET', 'POST'])
@login_required
def do_task(id):
    sess = db_session.create_session()
    task = sess.query(Tasks).filter(Tasks.id == id).first()
    if task.test:
        with open(task.path, 'r') as file:
            form = DoTheoryForm(json.load(file))
        return render_template('do_test.html', form=form, task=task)
    else:
        form = DoTheoryForm()
        with open(task.path, 'r') as file:
            text = file.read()
        return render_template('do_theory.html', text=text, task=task, form=form)


if __name__ == '__main__':
    main()
