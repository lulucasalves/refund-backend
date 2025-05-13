from models.event_status import EventStatus
from database.redis import redis_client
import json
from sqlalchemy.orm import Session
from utils.serialize_data import serialize_array


async def get_event_status_service(filters, db: Session):
    redis_key = "event-status"

    event_status_data = redis_client.get(redis_key)

    if event_status_data is None:
        event_status = db.query(EventStatus).all()
        serialized = serialize_array(event_status)

        redis_client.setex(
            redis_key,
            86400,
            json.dumps(serialized),
        )
    else:
        event_status = [
            EventStatus(**data) for data in json.loads(event_status_data)
        ]

    if "status" in filters:
        event_status = [c for c in event_status if c.status in filters["status"]]

    return event_status
