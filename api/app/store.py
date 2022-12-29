import redis
from app.config import settings

store = redis.Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_PASS
)


def get_store():

    return store
