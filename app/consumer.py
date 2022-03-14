import asyncio
from datetime import datetime

import aioredis
import json

redis_server = "redis://20.226.17.17"
redis = aioredis.from_url(redis_server, encoding="utf-8", decode_responses=True)

total_votes = 0


async def main():
    global total_votes
    async with redis.client() as conn:
        while True:
            chunk = []
            votes = {}
            for _ in range(0, 1000):
                item = await conn.lpop("votos")
                if item is not None:
                    obj = json.loads(item)
                    option = "votos_" + obj["body"].split("=")[1]
                    if option in votes:
                        votes[option] += 1
                    else:
                        votes[option] = 1
                    chunk.append(obj)
                else:
                    break
            if chunk:
                for option in votes.keys():
                    await conn.incrby(option, amount=votes[option])
                await conn.rpush("votos_bd", json.dumps(chunk))
                total_votes += len(chunk)
            else:
                return


if __name__ == "__main__":
    ini_time = datetime.now()
    asyncio.run(main())
    end_time = datetime.now()

    print("Apuração dos Votos")
    print(f"Total de Votos computados: {total_votes}")
    total_time = round((end_time - ini_time).seconds / 60, 2)
    print(f'Minutos processamento: {total_time}')
