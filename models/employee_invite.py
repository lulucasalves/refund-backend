from sqlalchemy import Column, String, DateTime, Boolean
import uuid


from database.mysql import Base


class EmployeeInvite(Base):
    __tablename__ = "employeeInvite"

    employeeInviteId = Column(
        String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    employeeId = Column(String(36))
    code = Column(String(30))
    confirmed=Column(Boolean)
    createdAt = Column(DateTime)
