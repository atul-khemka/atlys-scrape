import redis

from settings import Settings

settings = Settings()
r = redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0)

def get_client():
    try:
        r.ping()
        return r
    except (redis.exceptions.ConnectionError, ConnectionRefusedError) as e:
        raise e