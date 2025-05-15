from sqlalchemy import Column, String, DateTime
import uuid
from datetime import datetime
from database.mysql import Base


class EmployeeInvite(Base):
    __tablename__ = "employeeInvite"

    employeeInviteId = Column(
        String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    employeeId = Column(String(36))
    status = Column(String(30))
    createdAt = Column(DateTime, default=datetime.utcnow)
