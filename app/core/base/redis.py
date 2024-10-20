from typing import AsyncIterator
from redis import asyncio as aioredis


poolredis = aioredis.ConnectionPool.from_url(
    "redis://redis",
    decode_responses=True,
)
redis = aioredis.Redis(connection_pool=poolredis)

async def get_redis() -> AsyncIterator[aioredis.Redis]:
    try:
        yield redis
    finally:
        await redis.close()