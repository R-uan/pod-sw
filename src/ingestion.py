import asyncio
import redis.asyncio as redis
import json
from fetch_data import SWAPI
import normalize

_redis_client = None
async def get_redis():
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.Redis(
            host="localhost",
            port=6379,
            decode_responses=True
        )
    return _redis_client


# Name is which resource is being stored
# Data in this case will be all of the entries of each resource
# The entries should already be normalized to have their own id
# Redis Key: {name}:{data[i]["id"]}
async def store_resource(name, data):
  r = await get_redis();
  for entity in data:
   await r.set(f"wsapi:{name}:{entity["id"]}", json.dumps(entity))

async def fetch_resources():
  resources = [
      "people",
      "films",
      "starships",
      "vehicles",
      "species",
      "planets",
  ]

  tasks = [SWAPI.fetch_resources(name) for name in resources]
  results = await asyncio.gather(*tasks)

  for name, data in zip(resources, results):
    normalize.normalize_data(data)
    await store_resource(name, data)

