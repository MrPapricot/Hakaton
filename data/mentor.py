import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Mentor(SqlAlchemyBase):
    __tablename__ = 'mentors'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
