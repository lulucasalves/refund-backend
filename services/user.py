from fastapi import HTTPException
from datetime import datetime

from services.currency import get_currency_service
from models.user import User
from models.ambient import Ambient
from models.company import Company
from models.companyStatus import CompanyStatus
from models.dateFormat import DateFormat
from models.userCompany import UserCompany
from utils.serialize_data import serialize_array


async def find_user_auth_info(email, db):
    user = db.query(User).filter(User.email == email).first()

    if user is None:
        return None

    companies = (
        db.query(Company)
        .join(UserCompany, Company.companyId == UserCompany.companyId)
        .filter(UserCompany.userId == user.userId)
        .all()
    )

    ambients_ids = [c.ambientId for c in companies]
    ambients = db.query(Ambient).filter(Ambient.ambientId.in_(ambients_ids)).all()

    return {
        "user_id": user.userId,
        "email": user.email,
        "name": user.name,
        "last_ambient_id": user.lastAmbientId,
        "companies": [
            {"company_id": c.companyId, "name": c.name, "ambientId": c.ambientId}
            for c in companies
        ],
        "ambients": [{"ambient_id": a.ambientId, "name": a.name} for a in ambients],
    }


async def create_user(email, country, db):
    try:
        user_name = email.split("@")[0]

        ambient = Ambient(name=user_name)
        db.add(ambient)
        db.commit()
        db.refresh(ambient)

        status = db.query(CompanyStatus).filter(CompanyStatus.status == "Ativo").first()
        currency = serialize_array(
            await get_currency_service({"filters": {"countries": [country]}}, db)
        )[0]
        dateFormat = db.query(DateFormat).filter(DateFormat.country == country).first()

        company = Company(
            name="Company 1",
            dateFormatId=dateFormat.dateFormatId,
            currencyId=currency["currencyId"],
            statusId=status.statusId,
            ambientId=ambient.ambientId,
        )
        db.add(company)
        db.commit()
        db.refresh(company)

        user = User(
            name=user_name,
            email=email,
            lastAmbientId=ambient.ambientId,
            lastLogin=datetime.now(),
        )
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
