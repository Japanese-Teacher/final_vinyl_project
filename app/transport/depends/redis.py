import json
from typing import Optional, Any
import hashlib

from redis.asyncio import Redis

redis_client = Redis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True
)


def get_cache_key(prefix: str, **kwargs) -> str:
    key_str = f"{prefix}:{':'.join(f'{k}={v}' for k, v in sorted(kwargs.items()))}"
    return hashlib.md5(key_str.encode()).hexdigest()


async def get_cached_data(key: str) -> Optional[Any]:
    try:
        cached_data = await redis_client.get(key)
        if cached_data:
            return json.loads(cached_data)
        return None
    except Exception:
        return None


async def set_cached_data(key: str, data: Any, expire: int = 300) -> None:
    try:
        await redis_client.setex(key, expire, json.dumps(data))
    except Exception:
        pass


async def invalidate_cache(pattern: str) -> None:
    try:
        keys = await redis_client.keys(f"*{pattern}*")
        if keys:
            await redis_client.delete(*keys)
    except Exception:
        pass


async def close_redis():
    await redis_client.close()
