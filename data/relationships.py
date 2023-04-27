import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Relationship(SqlAlchemyBase):
    __tablename__ = 'relationships'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    task_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('tasks.id'), nullable=False)
    student_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('students.id'), nullable=False)
