from fetch_data import SWAPI
import functions_framework
import asyncio
import flask


@functions_framework.http
def star_wars_api(request: flask.Request):
  return asyncio.run(async_wrapper(request))


async def async_wrapper(request: flask.Request):
  path_parts = request.path.strip('/').split('/')
  if not path_parts or not path_parts[0]:
    return {'error': 'Path vazio'}, 400

  resource = path_parts[0]
  resource_id = path_parts[1] if len(path_parts) > 1 else None
  sub_resource = path_parts[2] if len(path_parts) > 2 else None

  valid_resources = [
      'people', 'planets', 'films', 'starships', 'vehicles', 'species'
  ]

  if resource not in valid_resources:
    return {
        'error': f"Recurso '{resource}' não existe",
        'recursos_validos': valid_resources
    }, 404

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

  return {'data': data}, 200
