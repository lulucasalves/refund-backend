from sqlalchemy.orm import Session
from fastapi import HTTPException

from models.user import User
from models.ambient import Ambient
from models.company import Company
from models.companyStatus import CompanyStatus
from models.dateFormat import DateFormat
from models.currency import Currency
from models.userCompany import UserCompany

import sys

sys.path.append("..")
from database.mysql import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def find_user(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        return None

    return {"userId": user.userId, "email": user.email}


async def create_new_user(email: str, db: Session):
    try:
        user_name = email.split("@")[0]

        ambient = Ambient(name=user_name)
        db.add(ambient)
        db.commit()
        db.refresh(ambient)

        status = db.query(CompanyStatus).filter(CompanyStatus.status == "Ativo").first()
        currency = db.query(Currency).filter(Currency.country == "US").first()
        dateFormat = db.query(DateFormat).filter(DateFormat.country == "US").first()

        company = Company(
            name="Company 1",
            dateFormatId=dateFormat.dateFormatId,
            currencyId=currency.currencyId,
            statusId=status.statusId,
            ambientId=ambient.ambientId,
        )
        db.add(company)
        db.commit()
        db.refresh(company)

        user = User(name=user_name, email=email)
        db.add(user)
        db.commit()
        db.refresh(user)

        userCompany = UserCompany(userId=user.userId, companyId=company.companyId)
        db.add(userCompany)
        db.commit()
        db.refresh(userCompany)

        return True
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
