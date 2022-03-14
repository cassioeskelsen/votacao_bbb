import asyncio
import uuid

import aioredis
import json
from datetime import datetime
from azure.storage.blob import BlobServiceClient

storage_url = "https://votosstorage.blob.core.windows.net/"
storage_name = "votosstorage"
# essa chave será rotacionada após a publicação do código :)
storage_key = "warLcMsccx8WLrxrCuJYlb5JXHPJxIto2OFKdSWvn1B+Nw3/LMPlrTMzzRaT7ryNYsbesLpcV272r5ZD7tUJZQ=="
storage_container = "votesdb"

service = BlobServiceClient(account_url=f"{storage_url}",
                            credential={"account_name": f"{storage_name}", "account_key": f"{storage_key}"})
container_client = service.get_container_client(storage_container)
destination_blob_client = container_client.get_blob_client(storage_container)

redis_server = "redis://20.226.17.17"
redis = aioredis.from_url(redis_server, encoding="utf-8", decode_responses=True)


async def main() -> dict:
    async with redis.client() as conn:
        while True:
            chunk = []
            for _ in range(0, 100):
                item = await conn.lpop("votos_bd")
                if item is not None:
                    chunk = chunk + json.loads(item)
                else:
                    break
            if chunk:
                block_id = str(uuid.uuid4())
                container_client.upload_blob(name=block_id, data=json.dumps(chunk))
            else:
                return


if __name__ == "__main__":
    ini_time = datetime.now()
    result = asyncio.run(main())
    end_time = datetime.now()

    print("Persistência dos Votos")
    total_time = round((end_time - ini_time).seconds / 60, 2)
    print(f'Minutos processamento: {total_time}')
