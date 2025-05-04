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
    try:
        db.begin()

        existing_companys = (
            db.query(Company)
            .join(UserCompany, UserCompany.companyId == Company.companyId)
            .filter(UserCompany.userId == userId, Company.ambientId == ambientId)
            .all()
        )

        companysCount = len(existing_companys)

        if companysCount - len(delete) + len(create) <= 0:
            raise HTTPException(status_code=400, detail="min_companys")

        for item in delete:
            user_company_to_delete = (
                db.query(UserCompany).filter(UserCompany.companyId == item).first()
            )
            company_to_delete = (
                db.query(Company).filter(Company.companyId == item).first()
            )

            if user_company_to_delete:
                db.delete(user_company_to_delete)
                db.commit()
            if company_to_delete:
                db.delete(company_to_delete)
                db.commit()

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

        new_companys = []
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
            new_companys.append(company)

        remaining_companys = (
            db.query(Company).filter(Company.ambientId == ambientId).count()
        )
        if remaining_companys == 0:
            raise HTTPException(status_code=400, detail="at_least_one_company_required")

        required_status_id = "c0246355-2708-11f0-9bf9-0242ac130002"
        has_required_status = (
            db.query(Company)
            .filter(
                Company.ambientId == ambientId, Company.statusId == required_status_id
            )
            .count()
            > 0
        )

        if not has_required_status:
            raise HTTPException(
                status_code=400,
                detail=f"at_least_one_company_must_have_status_{required_status_id}",
            )

        db.commit()
        return {"success": True}

    except HTTPException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
