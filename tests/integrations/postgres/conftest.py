import pytest
from httpx import AsyncClient

from app.models import VinylResponse
from tests.integrations.postgres.vinyl_test import VinylDTOFactory


@pytest.fixture
async def add_vinyl(
        client: AsyncClient,
)-> VinylResponse:
    vinyl_to_add = VinylDTOFactory.build()
    vinyl_json = vinyl_to_add.model_dump()
    response = await client.post('/vinyls', json=vinyl_json)
    response_json = response.json()
    return response_json