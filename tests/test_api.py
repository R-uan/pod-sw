import pytest
import sys
from pathlib import Path
from unittest.mock import AsyncMock, patch

# Importa os módulos do diretório src
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from main import async_wrapper


class TestResourceValidation:
  """Testes de validação de recursos"""

  @pytest.mark.asyncio
  async def test_empty_path_returns_400(self, mock_flask_request):
    """Deve retornar erro 400 para path vazio"""
    mock_flask_request.path = '/'
    mock_flask_request.args = {}

    response, status_code = await async_wrapper(mock_flask_request)

    assert status_code == 400
    assert 'error' in response

  @pytest.mark.asyncio
  async def test_invalid_resource_returns_404(self, mock_flask_request):
    """Deve retornar erro 404 para recurso inválido"""
    mock_flask_request.path = '/invalid_resource'
    mock_flask_request.args = {}

    response, status_code = await async_wrapper(mock_flask_request)

    assert status_code == 404
    assert 'error' in response
    assert 'valid_resources' in response


class TestFilterValidation:
  """Testes de validação de filtros"""

  @pytest.mark.asyncio
  async def test_invalid_filter_returns_400(self, mock_flask_request):
    """Deve retornar erro 400 para filtro inválido"""
    mock_flask_request.path = '/people'
    mock_flask_request.args = {'invalid_filter': 'value'}

    response, status_code = await async_wrapper(mock_flask_request)

    assert status_code == 400
    assert 'error' in response
    assert 'invalid_filters' in response

  @pytest.mark.asyncio
  async def test_valid_filter_accepted(self, mock_flask_request,
                                       sample_people_list):
    """Deve aceitar filtros válidos"""
    mock_flask_request.path = '/people'
    mock_flask_request.args = {'name': 'Luke'}

    with patch('main.SWAPI.fetch_resources',
               new_callable=AsyncMock) as mock_fetch:
      mock_fetch.return_value = sample_people_list

      response, status_code = await async_wrapper(mock_flask_request)

      assert status_code == 200
      assert 'data' in response


class TestListResources:
  """Testes para listagem de recursos"""

  @pytest.mark.asyncio
  async def test_fetch_all_people_without_filters(self, mock_flask_request,
                                                  sample_people_list):
    """Deve retornar todos os registros sem filtros"""
    mock_flask_request.path = '/people'
    mock_flask_request.args = {}

    with patch('main.SWAPI.fetch_resources',
               new_callable=AsyncMock) as mock_fetch:
      mock_fetch.return_value = sample_people_list.copy()

      response, status_code = await async_wrapper(mock_flask_request)

      assert status_code == 200
      assert 'data' in response

  @pytest.mark.asyncio
  async def test_filter_people_by_name(self, mock_flask_request,
                                       sample_people_list):
    """Deve filtrar pessoas por nome (case-insensitive)"""
    mock_flask_request.path = '/people'
    mock_flask_request.args = {'name': 'luke'}

    with patch('main.SWAPI.fetch_resources',
               new_callable=AsyncMock) as mock_fetch:
      mock_fetch.return_value = sample_people_list.copy()

      response, status_code = await async_wrapper(mock_flask_request)
      print(response)
      assert status_code == 200
