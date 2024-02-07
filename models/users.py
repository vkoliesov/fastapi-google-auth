import sqlalchemy as sa

from db import Base
from models.base import BaseMixin


class User(BaseMixin, Base):
    __tablename__ = "users"

    email = sa.Column(sa.String(120), unique=True)
    password = sa.Column(sa.String(255))
    first_name = sa.Column(sa.String(200))
    last_name = sa.Column(sa.String(200))
