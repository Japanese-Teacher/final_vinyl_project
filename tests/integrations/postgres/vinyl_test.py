import pytest
from httpx import AsyncClient
from polyfactory.factories.pydantic_factory import ModelFactory
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import VinylDTO


class VinylDTOFactory(ModelFactory[VinylDTO]):
    __model__ = VinylDTO

@pytest.mark.asyncio
async def test_add_vinyl_success(
        client: AsyncClient,
        async_session: AsyncSession,
)-> None:
    vinyl_to_add = VinylDTOFactory.build()
    vinyl_dict = vinyl_to_add.model_dump()
    response = await client.post(
        "/vinyls",
        json=vinyl_dict
    )
    assert response.status_code == 200
    assert response.json()["album_name"] == vinyl_dict["album_name"]
    result = await async_session.execute(select(VinylDTO))
    assert len(result.scalars().all()) == 1

@pytest.mark.asyncio
async def test_get_vinyl_by_id_success(
        client: AsyncClient, add_vinyl):
    created_vinyl = add_vinyl
    response = await client.get(f"/vinyls/{created_vinyl["id"]}")
    assert response.status_code == 200
    retrieved_vinyl = response.json()
    assert retrieved_vinyl["id"] == created_vinyl["id"]
    assert retrieved_vinyl["album_name"] == created_vinyl["album_name"]
    assert retrieved_vinyl["artist"] == created_vinyl["artist"]
    assert retrieved_vinyl["producer"] == created_vinyl["producer"]
    assert retrieved_vinyl["cost"] == created_vinyl["cost"]
    assert retrieved_vinyl["description"] == created_vinyl["description"]
    assert isinstance(retrieved_vinyl, dict)

@pytest.mark.asyncio
async def test_update_vinyl_success(client, add_vinyl):
    created_vinyl = add_vinyl
    vinyl_to_update = VinylDTOFactory.build()
    vinyl_json = vinyl_to_update.model_dump()
    response = await client.put(
        f'/vinyls/{created_vinyl["id"]}',
        json=vinyl_json,
    )
    assert response.status_code == 200
    get_response = await client.get(f"/vinyls/{created_vinyl["id"]}")
    assert get_response.status_code == 200
    retrieved_vinyl = get_response.json()
    assert retrieved_vinyl["id"] == created_vinyl["id"]
    assert retrieved_vinyl["album_name"] == vinyl_json["album_name"]
    assert retrieved_vinyl["artist"] == vinyl_json["artist"]
    assert retrieved_vinyl["producer"] == vinyl_json["producer"]
    assert retrieved_vinyl["cost"] == vinyl_json["cost"]
    assert retrieved_vinyl["description"] == vinyl_json["description"]
    assert isinstance(retrieved_vinyl, dict)

@pytest.mark.asyncio
async def test_delete_vinyl_success(client, add_vinyl):
    created_vinyl = add_vinyl
    response = await client.delete(f'/vinyls/{created_vinyl["id"]}')
    assert response.status_code == 200
    get_response = await client.get(f'/vinyls/{created_vinyl["id"]}')
    assert get_response.status_code == 404