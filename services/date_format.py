from models.date_format import DateFormat
from database.redis import redis_client
import json
from sqlalchemy.orm import Session
from utils.serialize_data import serialize_array


async def get_date_format_service(filters, db: Session):
    redis_key = "date-format"

    date_format_data = redis_client.get(redis_key)

    if date_format_data is None:
        date_format = db.query(DateFormat).all()
        serialized = serialize_array(date_format)

        redis_client.setex(
            redis_key,
            86400,
            json.dumps(serialized),
        )
    else:
        date_format = [
            DateFormat(**data) for data in json.loads(date_format_data)
        ]

    if "countries" in filters:
        date_format = [c for c in date_format if c.country in filters["countries"]]

    return date_format
