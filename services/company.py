from sqlalchemy.orm import Session
from models.company import Company
from models.user_company import UserCompany
from fastapi import HTTPException


async def get_company_service(filters, userId, db: Session):
    query = db.query(Company).join(
        UserCompany, UserCompany.companyId == Company.companyId
    )

    query = query.filter(UserCompany.userId == userId)
    query = query.filter(Company.ambientId == filters["ambientId"])

    if filters.get("statusId"):
        query = query.filter(Company.statusId.in_(filters["statusId"]))

    companies = query.all()

    return companies


async def update_company_service(create, edit, delete, ambientId, userId, db: Session):
    for item in create:
        if (
            isinstance(item, dict)
            and "name" in item
            and "statusId" in item
            and "currencyId" in item
            and "dateFormatId" in item
        ):
            company = Company(
                name=item["name"],
                dateFormatId=item["dateFormatId"],
                currencyId=item["currencyId"],
                statusId=item["statusId"],
                ambientId=ambientId,
            )
            db.add(company)
            db.commit()
            db.refresh(company)

            user_company = UserCompany(userId=userId, companyId=company.companyId)
            db.add(user_company)
            db.commit()
            db.refresh(user_company)
        else:
            raise HTTPException(
                status_code=400, detail="ausent_credentials_create_company"
            )

    for item in delete:
        user_company_to_delete = (
            db.query(UserCompany).filter(UserCompany.companyId == item).first()
        )
        company_to_delete = db.query(Company).filter(Company.companyId == item).first()
        db.delete(user_company_to_delete)
        db.commit()
        db.delete(company_to_delete)
        db.commit()

    for item in edit:
        company_to_edit = (
            db.query(Company).filter(Company.companyId == item["companyId"]).first()
        )

        if "name" in item:
            company_to_edit.name = item["name"]
        if "statusId" in item:
            company_to_edit.statusId = item["statusId"]
        if "currencyId" in item:
            company_to_edit.currencyId = item["currencyId"]
        if "dateFormatId" in item:
            company_to_edit.dateFormatId = item["dateFormatId"]

        db.commit()
        db.refresh(company_to_edit)

    result = {"success": True}

    return result
