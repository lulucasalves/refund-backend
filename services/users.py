from sqlalchemy.orm import Session
from models.user import User
import sys

sys.path.append("..")
from database.mysql import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def find_user(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()
