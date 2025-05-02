from models.currency import Currency
from database.redis import redis_client
import json
from sqlalchemy.orm import Session
from utils.serialize_data import serialize_array


async def get_currency_service(filters, db: Session):
    redis_key = "currencies"

    currencies_data = redis_client.get(redis_key)

    if currencies_data is None:
        currencies = db.query(Currency).all()
        serialized = serialize_array(currencies)

        redis_client.setex(
            redis_key,
            86400,
            json.dumps(serialized),
        )
    else:
        currencies = [Currency(**data) for data in json.loads(currencies_data)]

    if "countries" in filters:
        currencies = [c for c in currencies if c.country in filters["countries"]]
    if "symbols" in filters:
        currencies = [c for c in currencies if c.country in filters["symbols"]]

    return currencies
