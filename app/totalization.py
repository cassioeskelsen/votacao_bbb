import asyncio
from datetime import datetime

import aioredis
import json

redis_server = "redis://20.226.17.17"
redis = aioredis.from_url(
    redis_server, encoding="utf-8", decode_responses=True
)


async def main() -> dict:
    async with redis.client() as conn:
        keys = await conn.keys("votos_*")
        print(keys)
        for key in keys:
            print("Votos de "+key.split("_")[1] + " - " + await conn.get(key))


if __name__ == "__main__":
    result = asyncio.run(main())

