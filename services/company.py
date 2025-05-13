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

    query = query.order_by(Company.createdAt.desc())

    companies = query.all()

    return companies


async def delete_company_service(delete, db: Session):
    for item in delete:
        user_company_to_delete = (
            db.query(UserCompany).filter(UserCompany.companyId == item).first()
        )
        company_to_delete = db.query(Company).filter(Company.companyId == item).first()

        if user_company_to_delete:
            db.delete(user_company_to_delete)
            db.commit()
        if company_to_delete:
            db.delete(company_to_delete)
            db.commit()


async def edit_company_service(edit, db: Session):
    for item in edit:
        company_to_edit = (
            db.query(Company).filter(Company.companyId == item["id"]).first()
        )
        if not company_to_edit:
            continue

        if "name" in item:
            company_to_edit.name = item["name"]
        if "statusId" in item:
            company_to_edit.statusId = item["statusId"]
        if "currencyId" in item:
            company_to_edit.currencyId = item["currencyId"]
        if "dateFormatId" in item:
            company_to_edit.dateFormatId = item["dateFormatId"]

        db.add(company_to_edit)
        db.commit()


async def create_company_service(create, ambientId, userId, db: Session):
    for item in create:
        if not (
            isinstance(item, dict)
            and "name" in item
            and "statusId" in item
            and "currencyId" in item
            and "dateFormatId" in item
        ):
            raise HTTPException(
                status_code=400, detail="ausent_credentials_create_company"
            )

        company = Company(
            name=item["name"],
            dateFormatId=item["dateFormatId"],
            currencyId=item["currencyId"],
            statusId=item["statusId"],
            ambientId=ambientId,
        )
        db.add(company)
        db.flush()

        user_company = UserCompany(userId=userId, companyId=company.companyId)
        db.add(user_company)
        db.commit()


async def update_company_service(create, edit, delete, ambientId, userId, db: Session):
    try:
        db.begin()

        await delete_company_service(delete, db)
        await edit_company_service(edit, db)
        await create_company_service(create, ambientId, userId, db)

        return {"success": True}

    except HTTPException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
