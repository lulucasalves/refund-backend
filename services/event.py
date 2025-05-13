from sqlalchemy.orm import Session
from models.event import Event
from models.user_company import UserCompany
from fastapi import HTTPException


async def get_event_service(filters, userId, db: Session):
    query = db.query(Event).join(UserCompany, UserCompany.companyId == Event.companyId)

    query = query.filter(UserCompany.userId == userId)
    query = query.filter(Event.companyId == filters["companyId"])

    if filters.get("statusId"):
        query = query.filter(Event.statusId.in_(filters["statusId"]))

    query = query.order_by(Event.createdAt.desc())

    events = query.all()

    return events


async def delete_event_service(delete, db: Session):
    for item in delete:
        event_to_delete = db.query(Event).filter(Event.eventId == item).first()

        if event_to_delete:
            db.delete(event_to_delete)
            db.commit()


async def edit_event_service(edit, db: Session):
    for item in edit:
        event_to_edit = db.query(Event).filter(Event.eventId == item["id"]).first()
        if not event_to_edit:
            continue

        if "name" in item:
            event_to_edit.name = item["name"]
        if "statusId" in item:
            event_to_edit.statusId = item["statusId"]
        if "startDate" in item:
            event_to_edit.startDate = item["startDate"]
        if "endDate" in item:
            event_to_edit.endDate = item["endDate"]

        db.add(event_to_edit)
        db.commit()


async def create_event_service(create, companyId, db: Session):
    for item in create:
        if not (
            isinstance(item, dict)
            and "name" in item
            and "statusId" in item
            and "startDate" in item
            and "endDate" in item
        ):
            raise HTTPException(
                status_code=400, detail="ausent_credentials_create_event"
            )

        event = Event(
            name=item["name"],
            startDate=item["startDate"],
            endDate=item["endDate"],
            statusId=item["statusId"],
            companyId=companyId,
        )
        db.add(event)
        db.commit()


async def update_event_service(create, edit, delete, companyId, db: Session):
    try:
        db.begin()

        await delete_event_service(delete, db)
        await edit_event_service(edit, db)
        await create_event_service(create, companyId, db)

        return {"success": True}

    except HTTPException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
