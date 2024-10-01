import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from uuid import uuid4
from unittest.mock import patch, MagicMock
import bson
import pytest
from fastapi import HTTPException
from api.models.CattleModels import Cattle
from api.services.farm.cattle import read_cattle, read_all_cattles


@pytest.fixture
def mock_mongo():
    """Configura um mock para a conexão MongoDB."""
    with patch("api.services.farm.cattle.read.connect_mongo") as mock_connect_mongo:
        mock_collection = MagicMock()
        mock_client = MagicMock()
        mock_connect_mongo.return_value = (mock_collection, mock_client)

        yield mock_collection


@pytest.mark.asyncio
async def test_read_cattle_success(mock_mongo):
    """Testa a leitura de um gado com sucesso."""
    farm_id = uuid4()
    matrix_number = 172

    mock_mongo.find_one.return_value = {
        "_id": bson.ObjectId(),
        "number": matrix_number,
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

    cattle = await read_cattle(farm_id, matrix_number)

    assert isinstance(cattle, Cattle)
    assert cattle.number == matrix_number
    assert cattle.breed == "Angus"
    assert cattle.annotation == "Healthy cattle"
    assert cattle.age == 500
    assert len(cattle.weights) == 1


@pytest.mark.asyncio
async def test_read_cattle_not_found(mock_mongo):
    """Testa a leitura de um gado que não existe."""
    farm_id = uuid4()
    matrix_number = 999

    mock_mongo.find_one.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await read_cattle(farm_id, matrix_number)

    assert exc_info.value.status_code == 404
    assert (
        str(exc_info.value.detail)
        == f"Cattle with number {matrix_number} not found in farm {farm_id}"
    )


@pytest.mark.asyncio
async def test_read_all_cattles_success(mock_mongo):
    """Testa a leitura de todos os gados de uma fazenda com sucesso."""
    farm_id = uuid4()

    mock_mongo.find.return_value = [
        {
            "_id": bson.ObjectId(),
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
        },
        {
            "_id": bson.ObjectId(),
            "number": 173,
            "breed": "Hereford",
            "annotation": "Sick cattle",
            "age": 300,
            "weights": [
                {
                    "date": "2024-09-17 22:00:59.930176",
                    "weight": 450.0,
                    "observation": "Initial weight",
                }
            ],
            "farm_id": str(farm_id),
        },
    ]

    cattle_list = await read_all_cattles(farm_id)

    assert len(cattle_list) == 2
    assert isinstance(cattle_list[0], Cattle)
    assert cattle_list[0].number == 172
    assert cattle_list[1].number == 173


@pytest.mark.asyncio
async def test_read_all_cattles_not_found(mock_mongo):
    """Testa a leitura de gados quando nenhum é encontrado."""
    farm_id = uuid4()

    mock_mongo.find.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await read_all_cattles(farm_id)

    assert exc_info.value.status_code == 404
    assert str(exc_info.value.detail) == f"Cattles not found in farm {farm_id}"
