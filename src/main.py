import functions_framework
import asyncio
import flask

from swapi import SWAPI

# Comentarios estão em inglês por que é como eu normalmente penso na hora de fazer software;

# Remove related url array from data
# data = json object
# relations = array of propertie names
# To get their related entities request: /{resource}/{id}/{related}
def remove_relation_url(data, relations):
  for relation in relations:
    del data[relation]


@functions_framework.http
def star_wars_api(request: flask.Request):
  return asyncio.run(async_wrapper(request))


resources = {
    "people": {
        "name": "people",
        "singular": "person",
        "relationships": ["species", "films", "starships", "vehicles"],
        "filterable": ["name", "eye_color", "gender", "hair_color", "skin_color"],
    },
    "planets": {
        "name": "planets",
        "singular": "planet",
        "relationships": ["residents", "films"],
        "filterable": ["climate", "name", "terrain"],
    },
    "films": {
        "name": "films",
        "singular": "film",
        "filterable": ["title", "director", "producer", "year"],
        "relationships":
        ["characters", "planets", "species", "starships", "vehicles"],
    },
    "starships": {
        "name": "starships",
        "singular": "starship",
        "filterable": ["name", "model"],
        "relationships": ["films", "pilots"],
    },
    "vehicles": {
        "name": "vehicles",
        "singular": "vehicle",
        "filterable": ["name", "model", "class"],
        "relationships": ["films", "pilots"],
    },
    "species": {
        "name": "species",
        "singular": "specie",
        "filterable":
        ["name", "classification", "eye_color", "hair_color", "designation"],
        "relationships": ["people", "films"],
    }
}


async def async_wrapper(request: flask.Request):
  try:
    path_parts = request.path.strip('/').split('/')

    # If request path is empty
    if not path_parts or not path_parts[0]:
      return {'error': 'Path vazio'}, 400

    main_resource = resources.get(path_parts[0]) 
    main_resource_id = path_parts[1] if len(path_parts) > 1 else None
    related_resource = path_parts[2] if len(path_parts) > 2 else None
    
    # If the main resource is none
    if main_resource is None:
      return {
          'error': f"'{path_parts[0]} does not exist'",
          'valid_resources': resources.keys()
      }, 404

    # Get the name of each filter argument
    filter_parameters = request.args.keys()
    # resources[resource] should always be valid cause we checked it beforehand.
    invalid_filters = [p for p in filter_parameters if p not in main_resource["filterable"]]
    
    # If an invalid filter is given, return an error to let the client know
    if invalid_filters:
      return {
          'error': 'Invalid Parameters',
          'invalid_filters': invalid_filters,
          'filterables': main_resource["filterable"]
      }, 400
    
    if main_resource_id is None: 
      # Fetch all entries of the resource;
      data = await SWAPI.fetch_resources(main_resource["name"])

      # If the data contains entries and filter are present, apply the filters.
      if len(data) > 0 and len(filter_parameters) > 0:
        for key in request.args:
          value = request.args.get(key)
          if value is not None:
            data = [
                entry for entry in data
                if entry[key] is not None and value.lower() in entry[key].lower()
            ]

      for entry in data:
        remove_relation_url(entry, main_resource["relationships"])

      return {'data': data}, 200
    
    # Check for if the main resource has the related resource property before requesting it. 
    if related_resource is not None and related_resource not in main_resource["relationships"]:
      return {"error": f"{main_resource["name"]} does not have {related_resource}"}

    # Request target resource; return 404 if not found. 
    data = await SWAPI.fetch_resource(main_resource["name"], main_resource_id)
    if data is None: return { 'data': f"{main_resource} not found" }, 404
    
    # If no related field was requested then we can just return the data.
    if related_resource is None:
      remove_relation_url(data, main_resource["relationships"])
      return {"data": data}
    
    # Fetch related field urls 
    data = await SWAPI.fetch_list(data[related_resource])
    for entry in data: remove_relation_url(entry, resources[related_resource]["relationships"])

    return {"data": data}
  except:
    return { "error": "An unexpected error has ocurred"}, 500
