from typing import Annotated

from fastapi import Depends

from app.integrations.postgres.vinyl_repository import VinylRepository
from app.models import VinylDTO, VinylResponse


class VinylService:
    def __init__(
            self,
            vinyl_repository: Annotated[VinylRepository, Depends(VinylRepository)]
    ):
        self.vinyl_repository = vinyl_repository

    async def add_vinyl(self, vinyl: VinylDTO) -> VinylResponse:
        if await self.vinyl_repository.vinyl_exists(
                vinyl.album_name,
                vinyl.artist
        ):
            raise ValueError ("Vinyl record already exists")
        return await self.vinyl_repository.add_vinyl(vinyl)

    async def get_vinyl_by_id(self, vinyl_id: int)-> VinylResponse:
        if not await self.vinyl_repository.vinyl_by_id_exists(vinyl_id):
            raise ValueError ("Vinyl record does not exist")
        return await self.vinyl_repository.get_vinyl_by_id(vinyl_id)

    async def update_vinyl(
            self,
            vinyl_id: int,
            new_vinyl: VinylDTO
    ) -> VinylResponse:
        if not await self.vinyl_repository.vinyl_by_id_exists(vinyl_id):
            raise ValueError("Vinyl record does not exist")
        return await self.vinyl_repository.update_vinyl(vinyl_id, new_vinyl)

    async def delete_vinyl(
            self,
            vinyl_id: int,
    ) -> str:
        if not await self.vinyl_repository.vinyl_by_id_exists(vinyl_id):
            raise ValueError("Vinyl record does not exist")
        return await self.vinyl_repository.delete_vinyl(vinyl_id)