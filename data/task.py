import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Tasks(SqlAlchemyBase):
    __tablename__ = 'tasks'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    path = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    deadline = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    test = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True, default=False)