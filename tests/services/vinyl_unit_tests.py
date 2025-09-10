from unittest.mock import AsyncMock

import pytest

from app.services.vinyl_service import VinylService
from tests.integrations.postgres.vinyl_test import VinylDTOFactory


async def test_add_vinyl_success(
        mock_repo: AsyncMock,
        vinyl_service: VinylService,
) -> None:
    vinyl_to_add = VinylDTOFactory.build()
    mock_repo.vinyl_exists.return_value = False
    await vinyl_service.add_vinyl(vinyl_to_add)
    mock_repo.add_vinyl.assert_awaited_once_with(vinyl_to_add)

async def test_add_vinyl_duplicate_raises(
        mock_repo: AsyncMock,
        vinyl_service: VinylService
) -> None:
    vinyl_to_add = VinylDTOFactory.build()
    mock_repo.vinyl_exists.return_value = True
    with pytest.raises(ValueError, match="Vinyl record already exist"):
        await  vinyl_service.add_vinyl(vinyl_to_add)
    mock_repo.add_book.assert_not_awaited()


async def test_get_vinyl_by_id_success(
        mock_repo: AsyncMock,
        vinyl_service: VinylService
) -> None:
    mock_repo.vinyl_by_id_exists.return_value = True
    await vinyl_service.get_vinyl_by_id(1)
    mock_repo.get_vinyl_by_id.assert_awaited_once_with(1)

async def test_get_vinyl_not_exist_raises(
        mock_repo: AsyncMock,
        vinyl_service: VinylService
) -> None:
    mock_repo.vinyl_by_id_exists.return_value = False
    with pytest.raises(ValueError, match="Vinyl record does not exist"):
        await vinyl_service.get_vinyl_by_id(1)
    mock_repo.get_vinyl_by_id.assert_not_awaited()


async def test_update_vinyl_success(
        mock_repo: AsyncMock,
        vinyl_service: VinylService,
) -> None:
    vinyl_to_update = VinylDTOFactory.build()
    mock_repo.vinyl_by_id_exists.return_value = True
    await vinyl_service.update_vinyl(1, vinyl_to_update)
    mock_repo.update_vinyl.assert_awaited_once_with(1, vinyl_to_update)

async def test_update_vinyl_not_exist_raises(
        mock_repo: AsyncMock,
        vinyl_service: VinylService,
) -> None:
    vinyl_to_update = VinylDTOFactory.build()
    mock_repo.vinyl_by_id_exists.return_value = False
    with pytest.raises(ValueError, match="Vinyl record does not exist"):
        await vinyl_service.update_vinyl(1, vinyl_to_update)
    mock_repo.update_vinyl.assert_not_awaited()

async def test_delete_vinyl_success(
        mock_repo: AsyncMock,
        vinyl_service: VinylService,
) -> None:
    mock_repo.vinyl_by_id_exists.return_value = True
    await vinyl_service.delete_vinyl(1)
    mock_repo.delete_vinyl.assert_awaited_once_with(1)

async def test_delete_vinyl_not_exist_raises(
        mock_repo: AsyncMock,
        vinyl_service: VinylService,
) -> None:
    mock_repo.vinyl_by_id_exists.return_value = False
    with pytest.raises(ValueError, match="Vinyl record does not exist"):
        await vinyl_service.delete_vinyl(1)
    mock_repo.delete_vinyl.assert_not_awaited()