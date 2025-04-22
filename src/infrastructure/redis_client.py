from redis.asyncio import Redis


class RedisClient:
    _client: Redis | None = None

    @classmethod
    def create(cls, url: str) -> None:
        if cls._client:
            raise ValueError("Redis client already created")
        cls._client = Redis.from_url(url)

    @classmethod
    def get(cls) -> Redis:
        if not cls._client:
            raise ValueError("Redis client not initialized. Call create() first")
        return cls._client

    @classmethod
    async def close(cls) -> None:
        if not cls._client:
            return
        await cls._client.close()
        cls._client = None
