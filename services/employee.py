from sqlalchemy.orm import Session
from models.employee import Employee
from models.user import User
from models.user_company import UserCompany
from fastapi import HTTPException
from utils.format_date import format_date
from services.user import create_user
from services.employee_invite import send_verify_code
from models.employee_invite import EmployeeInvite


async def remove_employee_conditions(employee_id, user_id, company_id, db=Session):
    employee_invite = (
        db.query(EmployeeInvite)
        .filter(EmployeeInvite.employeeId == employee_id)
        .first()
    )
    if employee_invite:
        db.delete(employee_invite)

    user_company = (
        db.query(UserCompany)
        .filter(UserCompany.userId == user_id)
        .filter(UserCompany.companyId == company_id)
        .first()
    )
    print(user_company)
    if user_company:
        db.delete(user_company)
    db.commit()


def get_user_by_email(email, db):
    return db.query(User).filter(User.email == email).first()


async def get_employee_service(filters, user_id, db: Session):
    query = (
        db.query(Employee, User.email)
        .join(UserCompany, UserCompany.companyId == Employee.companyId)
        .join(User, User.userId == Employee.userId)
        .filter(UserCompany.userId == user_id)
        .filter(Employee.companyId == filters["companyId"])
        .order_by(Employee.createdAt.desc())
    )

    results = query.all()

    employees = []
    for employee, user_email in results:
        employee_dict = {**employee.__dict__}
        employee_dict["email"] = user_email
        employees.append(employee_dict)

    return employees


async def delete_employee_service(delete, company_id, db: Session):
    for item in delete:
        employee_to_delete = (
            db.query(Employee).filter(Employee.employeeId == item).first()
        )

        if employee_to_delete:
            await remove_employee_conditions(
                employee_to_delete.employeeId, employee_to_delete.userId, company_id, db
            )
            db.delete(employee_to_delete)
            db.commit()


async def edit_employee_service(edit, company_id, db: Session):
    for item in edit:
        employee_to_edit = (
            db.query(Employee).filter(Employee.employeeId == item["id"]).first()
        )
        if not employee_to_edit:
            continue

        if "name" in item:
            employee_to_edit.name = item["name"]
        if "email" in item:
            user = db.query(User).filter(User.userId == employee_to_edit.userId).first()

            if user.email != item["email"]:
                employee_to_edit.verification = "pending"
                await remove_employee_conditions(
                    employee_to_edit.employeeId, employee_to_edit.userId, company_id, db
                )
                user = get_user_by_email(item["email"], db)
                if user is None:
                    await create_user(item["email"], "US", db)
                    user = get_user_by_email(item["email"], db)

                await send_verify_code(employee_to_edit.employeeId, db)
                employee_to_edit.userId = user.userId
        if "document" in item:
            employee_to_edit.document = format_date(item["document"])
        if "phone" in item:
            employee_to_edit.phone = format_date(item["phone"])

        db.add(employee_to_edit)
        db.commit()


async def create_employee_service(create, company_id, db: Session):
    for item in create:
        if not (
            isinstance(item, dict)
            and "name" in item
            and "email" in item
            and "document" in item
        ):
            raise HTTPException(
                status_code=400, detail="ausent_credentials_create_employee"
            )

        user = get_user_by_email(item["email"], db)

        if user is None:
            await create_user(item["email"], "US", db)
            user = get_user_by_email(item["email"], db)

        employee = Employee(
            name=item["name"],
            document=item["document"],
            phone=item.get("phone"),
            userId=user.userId,
            verification="pending",
            companyId=company_id,
        )
        db.add(employee)
        db.commit()
        db.refresh(employee)

        await send_verify_code(employee.employeeId, db)
        db.commit()


async def update_employee_service(create, edit, delete, company_id, db: Session):
    try:
        db.begin()

        await delete_employee_service(delete, company_id, db)
        await edit_employee_service(edit, company_id, db)
        await create_employee_service(create, company_id, db)

        return {"success": True}

    except HTTPException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
