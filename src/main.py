from fastapi import FastAPI
import asyncio
import json

from fetch_data import SWAPI
import normalize

app = FastAPI()


@app.get("/")
async def root():
  return {"message": "Hello World"}


async def main():
  return 0


async def fetch_resources():
  resources = [
      "people",
      "films",
      "starships",
      "vehicles",
      "species",
      "planets",
  ]

  tasks = [SWAPI.fetch_resource(name) for name in resources]
  results = await asyncio.gather(*tasks)

  for name, data in zip(resources, results):
    normalize.normalize_data(data)
    with open(f"data/{name}.json", "w", encoding="utf-8") as f:
      json.dump(data, f, indent=2, ensure_ascii=False)


asyncio.run(main())
