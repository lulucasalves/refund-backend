from sqlalchemy import Column, String
import uuid
from database.mysql import Base


class DateFormat(Base):
    __tablename__ = "dateFormat"

    dateFormatId = Column(
        String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    dateFormat = Column(String(10))
    country = Column(String(2))
