from sqlalchemy.orm import Session
from models.employee import Employee
from models.user_company import UserCompany
from models.company import Company
from fastapi import HTTPException
from models.employee_invite import EmployeeInvite


async def send_verify_code(employee_id, db=Session):
    employee_invite = EmployeeInvite(
        employeeId=employee_id,
        status="pending",
    )
    db.add(employee_invite)
    db.commit()


async def get_employee_invite_service(user_id, db):
    query = (
        db.query(EmployeeInvite, Company.name)
        .join(Employee, EmployeeInvite.employeeId == Employee.employeeId)
        .join(Company, Company.companyId == Employee.companyId)
        .filter(Employee.userId == user_id)
        .filter(EmployeeInvite.status == "pending")
    )

    results = query.all()

    employee_invite = []
    for employee, name in results:
        employee_dict = {**employee.__dict__}
        employee_dict["company"] = name
        employee_invite.append(employee_dict)

    return employee_invite


async def verify_employee_invite_service(employee_id, status, user_id, db: Session):
    print(status)
    employee_invite = (
        db.query(EmployeeInvite)
        .filter(EmployeeInvite.employeeId == employee_id)
        .first()
    )

    if employee_invite is None or employee_invite.status != "pending":
        raise HTTPException(
            status_code=400, detail="ausent_credentials_verify_employee"
        )

    if status != "verified" and status != "refused":
        raise HTTPException(status_code=400, detail="status_not_permited")

    employee = (
        db.query(Employee)
        .filter(Employee.employeeId == employee_invite.employeeId)
        .first()
    )

    if user_id != employee.userId:
        raise HTTPException(status_code=400, detail="user_not_found")

    employee.verification = status
    db.add(employee)

    employee_invite.status = status
    db.add(employee_invite)

    if status == "verified":
        user_company = UserCompany(userId=employee.userId, companyId=employee.companyId)
        db.add(user_company)

    db.commit()

    return {"success": True}
