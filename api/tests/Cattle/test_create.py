import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

import json
from uuid import uuid4
from unittest.mock import patch, MagicMock
import pytest
from api.models.CattleModels import CattleIn
from api.services.farm.cattle import create_cattle
from fastapi import HTTPException


CATTLE_JSON = """
{
    "number": 172,
    "breed": "Angus",
    "annotation": "Healthy cattle",
    "age": 500,
    "weights": {
        "date": "2024-09-17 22:00:59.930176",
        "weight": 500.0,
        "observation": "Initial weight"
    }
}
"""


@pytest.fixture
def cattle_data():
    """Retorna dados de gado convertidos de JSON para um dicionário."""
    return json.loads(CATTLE_JSON)


@pytest.fixture
def mock_mongo():
    """Configura um mock para a conexão MongoDB."""
    with patch("api.services.farm.cattle.create.connect_mongo") as mock_connect_mongo:
        mock_collection = MagicMock()
        mock_client = MagicMock()
        mock_connect_mongo.return_value = (mock_collection, mock_client)
        yield mock_collection


@pytest.mark.asyncio
async def test_create_cattle_with_json(cattle_data, mock_mongo):
    """Testa a criação de um gado com dados JSON."""
    cattle_in = CattleIn(**cattle_data)
    farm_id = uuid4()

    mock_mongo.insert_one.return_value.inserted_id = str(farm_id)

    inserted_id = await create_cattle(farm_id, cattle_in)

    assert inserted_id == str(farm_id)

    expected_data = {
        "number": 172,
        "breed": "Angus",
        "annotation": "Healthy cattle",
        "age": 500,
        "weights": [
            {
                "date": "2024-09-17 22:00:59.930176",
                "weight": 500.0,
                "observation": "Initial weight",
            }
        ],
        "farm_id": str(farm_id),
    }

    mock_mongo.insert_one.assert_called_once_with(expected_data)


@pytest.mark.asyncio
async def test_create_cattle_with_invalid_data(mock_mongo):
    """Testa a criação de um gado com dados inválidos, faltando number no caso."""
    invalid_cattle_data = {
        "breed": "Angus",
        "age": 500,
        "weights": {
            "date": "2024-09-17 22:00:59.930176",
            "weight": 500.0,
            "observation": "Initial weight",
        },
    }
    farm_id = uuid4()

    with pytest.raises(ValueError):
        cattle_in = CattleIn(**invalid_cattle_data)
        await create_cattle(farm_id, cattle_in)


@pytest.mark.asyncio
async def test_create_cattle_insertion_failure(cattle_data, mock_mongo):
    """Testa o comportamento quando a inserção no MongoDB falha."""
    cattle_in = CattleIn(**cattle_data)
    farm_id = uuid4()

    mock_mongo.insert_one.side_effect = Exception("Database error")

    with pytest.raises(HTTPException) as excinfo:
        await create_cattle(farm_id, cattle_in)

    assert excinfo.value.status_code == 500
    assert excinfo.value.detail == "Erro ao inserir dados: Database error"


@pytest.mark.asyncio
async def test_create_cattle_check_farm_id(cattle_data, mock_mongo):
    """Testa se o farm_id é salvo corretamente ao criar gado."""
    cattle_in = CattleIn(**cattle_data)
    farm_id = uuid4()

    mock_mongo.insert_one.return_value.inserted_id = str(farm_id)

    inserted_id = await create_cattle(farm_id, cattle_in)

    expected_data = {
        "number": 172,
        "breed": "Angus",
        "annotation": "Healthy cattle",
        "age": 500,
        "weights": [
            {
                "date": "2024-09-17 22:00:59.930176",
                "weight": 500.0,
                "observation": "Initial weight",
            }
        ],
        "farm_id": str(farm_id),
    }

    assert inserted_id == str(farm_id)
    mock_mongo.insert_one.assert_called_once_with(expected_data)
