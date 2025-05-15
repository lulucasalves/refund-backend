from sqlalchemy import Column, String, DateTime
import uuid
from datetime import datetime
from database.mysql import Base


class Company(Base):
    __tablename__ = "company"

    companyId = Column(
        String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    name = Column(String(100))
    statusId = Column(String(36))
    currencyId = Column(String(36))
    dateFormatId = Column(String(36))
    ambientId = Column(String(36))
    createdAt = Column(DateTime, default=datetime.utcnow)
