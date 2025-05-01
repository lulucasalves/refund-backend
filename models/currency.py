from sqlalchemy import Column, String
import uuid

import sys

sys.path.append("..")
from database.mysql import Base


class Currency(Base):
    __tablename__ = "currency"

    currencyId = Column(
        String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    symbol = Column(String(2))
    country = Column(String(2))
