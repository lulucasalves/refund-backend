from models.company_status import CompanyStatus
from database.redis import redis_client
import json
from sqlalchemy.orm import Session
from utils.serialize_data import serialize_array


async def get_company_status_service(filters, db: Session):
    redis_key = "company-status"

    company_status_data = redis_client.get(redis_key)

    if company_status_data is None:
        company_status = db.query(CompanyStatus).all()
        serialized = serialize_array(company_status)

        redis_client.setex(
            redis_key,
            86400,
            json.dumps(serialized),
        )
    else:
        company_status = [
            CompanyStatus(**data) for data in json.loads(company_status_data)
        ]

    if "status" in filters:
        company_status = [c for c in company_status if c.status in filters["status"]]

    return company_status
