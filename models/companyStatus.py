from sqlalchemy import Column, String
import uuid

import sys

sys.path.append("..")
from database.mysql import Base


class CompanyStatus(Base):
    __tablename__ = "companyStatus"

    statusId = Column(
        String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    status = Column(String(100))
