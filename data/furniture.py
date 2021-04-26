import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Furniture(SqlAlchemyBase):
    __tablename__ = 'furniture'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)      # Название
    content = sqlalchemy.Column(sqlalchemy.String, nullable=False)   # Описание
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)    # Цена
    amount = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)   # Кол-во
    photo = sqlalchemy.Column(sqlalchemy.String, nullable=False)     # Путь к фотографии
    tags = sqlalchemy.Column(sqlalchemy.String, nullable=False)

