import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from uuid import uuid4
from unittest.mock import patch, MagicMock
import pytest
from fastapi import HTTPException
from api.models.CattleModels import CattleUpdate, HealthHistory, Reproduction, Weight
from api.services.farm.cattle import update_cattle

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))


@pytest.fixture
def mock_mongo():
    """Configura um mock para a conexão MongoDB."""
    with patch("api.services.farm.cattle.update.connect_mongo") as mock_connect_mongo:
        mock_collection = MagicMock()
        mock_client = MagicMock()
        mock_connect_mongo.return_value = (mock_collection, mock_client)

        yield mock_collection


@pytest.mark.asyncio
async def test_update_cattle_success(mock_mongo):
    """Testa a atualização de um gado com sucesso."""
    farm_id = uuid4()
    matrix_number = 172

    mock_mongo.find_one.return_value = {
        "_id": "some-object-id",
        "number": matrix_number,
        "weights": [],
        "reproduction": [],
        "health_history": [],
        "farm_id": str(farm_id),
    }

    update_data = CattleUpdate(
        weights=Weight(date="2024-09-17", weight=600.0, observation="Updated weight"),
        reproduction=Reproduction(type="AI", date="2024-10-01"),
        health_history=HealthHistory(date="2024-10-01", status="Healthy"),
    )

    response = await update_cattle(farm_id, matrix_number, update_data)

    assert (
        response["message"]
        == f"Cattle with number {matrix_number} in farm {farm_id} updated successfully"
    )
    mock_mongo.update_one.assert_called_once()  # Verifica se o update_one foi chamado


@pytest.mark.asyncio
async def test_update_cattle_not_found(mock_mongo):
    """Testa a atualização de um gado que não existe."""
    farm_id = uuid4()
    matrix_number = 999  # Número que não existe

    mock_mongo.find_one.return_value = None

    update_data = CattleUpdate(
        weights=Weight(date="2024-09-17", weight=600.0, observation="Updated weight"),
        reproduction=Reproduction(type="AI", date="2024-10-01"),
        health_history=HealthHistory(date="2024-10-01", status="Healthy"),
    )

    mock_mongo.update_one.return_value.matched_count = 0

    with pytest.raises(HTTPException) as exc_info:
        await update_cattle(farm_id, matrix_number, update_data)

    assert exc_info.value.status_code == 500
    assert str(exc_info.value.detail) == "Error updating data."


@pytest.mark.asyncio
async def test_update_cattle_no_valid_fields(mock_mongo):
    """Testa a atualização sem campos válidos."""
    farm_id = uuid4()
    matrix_number = 172

    mock_mongo.find_one.return_value = {
        "_id": "some-object-id",
        "number": matrix_number,
        "weights": [],
        "reproduction": [],
        "health_history": [],
        "farm_id": str(farm_id),
    }

    update_data = CattleUpdate(
        weights=None,
        reproduction=None,
        health_history=None,
        number=None,  # Nenhum campo válido para atualização
    )

    with pytest.raises(HTTPException) as exc_info:
        await update_cattle(farm_id, matrix_number, update_data)

    assert exc_info.value.status_code == 500
    assert str(exc_info.value.detail) == "Error updating data."
