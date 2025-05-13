from sqlalchemy import Column, String
import uuid

from database.mysql import Base


class EventStatus(Base):
    __tablename__ = "eventStatus"

    statusId = Column(
        String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    status = Column(String(100))
