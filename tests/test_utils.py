import pytest

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from main import remove_relation_url


class TestRemoveRelationUrl:
  """Testes para a função remove_relation_url"""

  def test_remove_single_relation(self):
    """Deve remover uma relação do objeto"""
    data = {
        "name": "Luke",
        "films": ["film1", "film2"],
        "species": ["species1"]
    }
    relations = ["films"]

    remove_relation_url(data, relations)

    assert "films" not in data
    assert "species" in data
    assert data["name"] == "Luke"

  def test_remove_multiple_relations(self):
    """Deve remover múltiplas relações do objeto"""
    data = {
        "name": "Luke",
        "films": ["film1"],
        "species": ["species1"],
        "vehicles": ["vehicle1"],
        "starships": ["starship1"]
    }
    relations = ["films", "species", "vehicles", "starships"]

    remove_relation_url(data, relations)

    assert "films" not in data
    assert "species" not in data
    assert "vehicles" not in data
    assert "starships" not in data
    assert data["name"] == "Luke"

  def test_remove_nonexistent_relation(self):
    """Deve lançar KeyError ao tentar remover relação inexistente"""
    data = {"name": "Luke"}
    relations = ["films"]

    with pytest.raises(KeyError):
      remove_relation_url(data, relations)

  def test_empty_relations_array(self):
    """Deve manter o objeto intacto com array vazio"""
    data = {"name": "Luke", "films": ["film1"]}
    original_data = data.copy()
    relations = []

    remove_relation_url(data, relations)

    assert data == original_data
