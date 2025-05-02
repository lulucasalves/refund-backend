from sqlalchemy import Column, String, DateTime
import uuid
from database.mysql import Base


class User(Base):
    __tablename__ = "user"

    userId = Column(
        String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    name = Column(String(100))
    email = Column(String(100), unique=True)
    lastLogin = Column(DateTime)
    lastAmbientId = Column(String(36))
