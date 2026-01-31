def normalize_data(data):
  simplify_relations(data)
  # For some reason the objects do not have an ID field
  # but the url does have an unique numerical identifier
  # so we will extract that identifier from the URL and
  # use it as an id property.
  #
  # Every resource has an url property so we can reliably
  # do this operation o every entry.
  for entity in data:
    entity["id"] = extract_id_from_url(entity["url"])


# Because the urls are structured the same, we can extract each object
# id with this function from their url. Luckily, the url is present in
# the object itself so we can just get it.
def extract_id_from_url(url: str):
  try:
    # Split the URL.
    # The last url should be the index of
    # the resource that will be used as id
    parts = url.strip().split("/")
    value = int(parts[-2])
    return value
  except ValueError:
    return None


# Each resource has a array of URLs containing resources they are
# related to. Because we are using those URLs to create unique ids
# we can simplyfy their urls to the numerical identifier using the
# extraction method and replace the URL with the number.
def simplify_relations(data):
  relations = [
      "films", "pilots", "people", "residents", "starships", "vehicles",
      "species", "planets"
  ]

  for entity in data:
    for relation in relations:
      if relation in entity:
        for index, url in enumerate(entity[relation]):
          id = extract_id_from_url(url)
          entity[relation][index] = id
