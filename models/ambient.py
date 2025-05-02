from sqlalchemy import Column, String
import uuid

from database.mysql import Base


class Ambient(Base):
    __tablename__ = "ambient"

    ambientId = Column(
        String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    name = Column(String(100))
