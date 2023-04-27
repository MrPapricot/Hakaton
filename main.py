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

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/database.db")
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(student_id):
    db_sess = db_session.create_session()
    return db_sess.query(Student).get(student_id)


def main():
    app.run()


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


@app.route('/login', methods=['GET', 'POST'])
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


@app.route('/add_test')
@login_required
def add_test():
    if current_user.mentor:
        form = TestForm()
        if form.validate_on_submit():
            sess = db_session.create_session()
            task = Tasks()
            task.test = True
            task.test = form.title
            task.deadline = form.deadline
            file = form.file.data
            file.save('tasks/' + file.filename)
            task.path = 'tasks/' + file.filename
            students = [sess.query(Student).filter(Student.id == i).first() for i in form.students.data.split(', ')]
            sess.add(task)
            sess.commit()
            add_task(task=task, students=students)
            return redirect('/')
        return render_template('task.html', form=form)



if __name__ == '__main__':
    main()
