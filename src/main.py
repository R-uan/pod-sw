from fetch_data import SWAPI
import functions_framework
import asyncio
import flask
import json


@functions_framework.http
def star_wars_api(request: flask.Request):
  return asyncio.run(async_wrapper(request))


resources = {
    "people": {
        "fields": ["name", "eye_color", "gender", "hair_color", "skin_color"]
    },
    "planets": {
        "fields": ["climate", "name", "terrain"]
    },
    "films": {
        "fields": ["title", "director", "producer", "year"]
    },
    "starships": {
        "fields": ["name", "model"]
    },
    "vehicles": {
        "fields": ["name", "model", "class"]
    },
    "species": {
        "fields":
        ["name", "classification", "eye_color", "hair_color", "designation"]
    }
}


async def async_wrapper(request: flask.Request):
  path_parts = request.path.strip('/').split('/')
  if not path_parts or not path_parts[0]:
    return {'error': 'Path vazio'}, 400

  resource = path_parts[0]
  resource_id = path_parts[1] if len(path_parts) > 1 else None
  sub_resource = path_parts[2] if len(path_parts) > 2 else None

  if resource not in resources.keys():
    return {
        'error': f"Recurso '{resource}' não existe",
        'recursos_validos': resources.keys()
    }, 404

  # Parameters will be ignored in case of requests with specified id
  params_received = request.args.keys()
  # resources[resource] should always be valid cause we checked it beforehand.
  invalid_params = [
      p for p in params_received if p not in resources[resource]["fields"]
  ]

  if invalid_params:
    return {
        'error': 'Invalid Parameters',
        'invalid_params': invalid_params,
        'valid_params': resources[resource]["fields"]
    }, 400

  if resource_id is not None:
    data = await SWAPI.fetch_resource(resource, resource_id)

    if data is None:
      return {'error': f"{resource}: {resource_id} not found"}, 404

    if sub_resource is not None:
      singular = {
          "people": "person",
          "films": "film",
          "species": "specie",
          "vehicles": "vehicle",
          "planets": "planet",
          "starships": "starship"
      }

      if sub_resource not in data:
        return {
            'error':
            f"'{sub_resource}' is not available for this resource",
            'sub_recursos_disponiveis':
            [k for k in data.keys() if isinstance(data.get(k), list)]
        }, 400

      urls = data[sub_resource]

      name = data.get("name") if resource != "films" else data.get("title")

      if not urls or len(urls) == 0:
        return {
            singular.get(resource): name,
            sub_resource: [],
            'message': f'{singular.get(resource)} does not have {sub_resource}'
        }, 200

      # Busca sub-recursos em paralelo
      sub_resources = await SWAPI.fetch_list(urls)

      return {
          singular.get(resource): name,
          f"{singular.get(resource)}_id": resource_id,
          sub_resource: sub_resources,
          'total': len(sub_resources)
      }, 200
    return {"data": data}, 200

  data = await SWAPI.fetch_resources(resource)
  if len(data) > 0 and len(params_received) > 0:
    filtered = []
    for key in request.args:
      value = request.args.get(key)
      if value is not None:
        for entry in data:
          if entry[key] is not None and value.lower() in entry[key].lower():
            filtered.append(entry)
    return {'data': filtered}

  return {'data': data}, 200
