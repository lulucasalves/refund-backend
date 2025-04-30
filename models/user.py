from sqlalchemy import Column, Integer, String

import sys

sys.path.append("..")
from database.mysql import Base


class User(Base):
    __tablename__ = "user"

    userId = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True)
