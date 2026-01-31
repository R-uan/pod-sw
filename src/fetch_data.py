import httpx

base = "https://swapi.dev/api/"

class SWAPI:
    @staticmethod
    async def fetch_resource(resource):
        results = [];
        async with httpx.AsyncClient() as client:
            url = f"{base}/{resource}?page=1";
            while url:
                r = await client.get(url);
                data = r.json();
                results.extend(data["results"]);
                url = data["next"];
        return results;
