from unittest.mock import AsyncMock

import pytest


@pytest.fixture
def mock_repo():
    return AsyncMock()

@pytest.fixture
def vinyl_service(mock_repo):
    from app.services.vinyl_service import VinylService
    return VinylService(vinyl_repository=mock_repo)
