import httpx

base = "https://swapi.dev/api/"


class SWAPI:
  # fetch a list of urls
  @staticmethod
  async def fetch_list(urls):
    results = []
    async with httpx.AsyncClient() as client:
      for url in urls:
        response = await client.get(url)
        if response.status_code == 200:
          data = response.json()
          results.append(data)
    return results

  # Single entries
  @staticmethod
  async def fetch_resource(resource, id):
    async with httpx.AsyncClient() as client:
      url = f"{base}/{resource}/{id}"
      response = await client.get(url)
      if response.status_code == 404: return None
      return response.json()

  # All entries (deals with pagination)
  @staticmethod
  async def fetch_resources(resource):
    results = []
    async with httpx.AsyncClient() as client:
      url = f"{base}/{resource}/?page=1"
      while url:
        r = await client.get(url)
        if r.status_code != 200: return None
        data = r.json()
        results.extend(data["results"])
        url = data["next"]
    return results
