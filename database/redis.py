from redis import Redis
import os
from dotenv import load_dotenv

load_dotenv()


class RedisClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedisClient, cls).__new__(cls)
            cls._instance.init_connection()
        return cls._instance

    def init_connection(self):
        self.connection = Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            db=int(os.getenv("REDIS_DB", 0)),
            password=os.getenv("REDIS_PASSWORD", None),
            decode_responses=True,
        )

    def get_connection(self) -> Redis:
        return self.connection


redis_client = RedisClient().get_connection()
