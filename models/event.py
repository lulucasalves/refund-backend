from sqlalchemy import Column, String, DateTime
import uuid


from database.mysql import Base


class Event(Base):
    __tablename__ = "event"

    eventId = Column(
        String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    name = Column(String(100))
    statusId = Column(String(36))
    companyId = Column(String(36))
    startDate = Column(DateTime)
    endDate = Column(DateTime)
    createdAt = Column(DateTime)
