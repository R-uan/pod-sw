import pytest


@pytest.fixture
def sample_person():
  return {
      "name": "Luke Skywalker",
      "height": "172",
      "mass": "77",
      "hair_color": "blond",
      "skin_color": "fair",
      "eye_color": "blue",
      "birth_year": "19BBY",
      "gender": "male",
      "homeworld": "https://swapi.dev/api/planets/1/",
      "films":
      ["https://swapi.dev/api/films/1/", "https://swapi.dev/api/films/2/"],
      "species": [],
      "vehicles": ["https://swapi.dev/api/vehicles/14/"],
      "starships": ["https://swapi.dev/api/starships/12/"],
      "url": "https://swapi.dev/api/people/1/"
  }


@pytest.fixture
def sample_people_list():
  return [{
      "name": "Luke Skywalker",
      "eye_color": "blue",
      "gender": "male",
      "hair_color": "blond",
      "skin_color": "fair",
      "species": [],
      "films": [],
      "starships": [],
      "vehicles": []
  }, {
      "name": "Darth Vader",
      "eye_color": "yellow",
      "gender": "male",
      "hair_color": "none",
      "skin_color": "white",
      "species": [],
      "films": [],
      "starships": [],
      "vehicles": []
  }, {
      "name": "Leia Organa",
      "eye_color": "brown",
      "gender": "female",
      "hair_color": "brown",
      "skin_color": "light",
      "species": [],
      "films": [],
      "starships": [],
      "vehicles": []
  }]


@pytest.fixture
def sample_films():
  return [{
      "title": "A New Hope",
      "episode_id": 4,
      "director": "George Lucas",
      "characters": [],
      "planets": [],
      "species": [],
      "starships": [],
      "vehicles": []
  }, {
      "title": "The Empire Strikes Back",
      "episode_id": 5,
      "director": "Irvin Kershner",
      "characters": [],
      "planets": [],
      "species": [],
      "starships": [],
      "vehicles": []
  }]


@pytest.fixture
def mock_flask_request(mocker):
  return mocker.Mock()
