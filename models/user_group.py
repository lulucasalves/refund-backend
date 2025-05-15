from sqlalchemy import Column, String, Boolean
import uuid
from database.mysql import Base


class UserGroup(Base):
    __tablename__ = "userGroup"

    userGroupId = Column(
        String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    name = Column(String(100))
    canModify = Column(Boolean)
    companyId = Column(String(36))
