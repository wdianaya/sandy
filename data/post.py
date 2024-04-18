import sqlalchemy
import datetime
from sqlalchemy import orm

from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Post(SqlAlchemyBase, SerializerMixin):

    __tablename__ = 'posts'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    team_leader = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    posts = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    views = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    image_post = sqlalchemy.Column(sqlalchemy.String(50), nullable=False, default='default.jpg')
    start_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)


    def __repr__(self):
        return f'<Post> {self.id} {self.title} {self.posts}'