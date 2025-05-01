from sqlalchemy import Column, String
import uuid

import sys

sys.path.append("..")
from database.mysql import Base


class UserCompany(Base):
    __tablename__ = "userCompany"

    userCompanyId = Column(
        String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    userId = Column(String(100))
    companyId = Column(String(36))
