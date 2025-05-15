from sqlalchemy import Column, String, DateTime
import uuid
from datetime import datetime
from database.mysql import Base


class Employee(Base):
    __tablename__ = "employee"

    employeeId = Column(
        String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    name = Column(String(100))
    phone = Column(String(30))
    document = Column(String(30))
    verification = Column(String(30))
    userId = Column(String(36))
    companyId = Column(String(36))
    createdAt = Column(DateTime, default=datetime.utcnow)
