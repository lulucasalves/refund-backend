from sqlalchemy.orm import Session
from models.ambient import Ambient


async def update_ambient_service(name, ambientId, db: Session):
    ambient_to_edit = db.query(Ambient).filter(Ambient.ambientId == ambientId).first()

    ambient_to_edit.name = name

    db.commit()
    db.refresh(ambient_to_edit)

    result = {"success": True}

    return result
