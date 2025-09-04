from typing import Annotated

from fastapi import APIRouter, Depends

from app.models import VinylDTO
from app.services.vinyl_service import VinylService

vinyl_router = APIRouter(
    prefix='/vinyl',
    tags=["Vinyl"]
)


@vinyl_router.post('', response_model=VinylDTO)
async def add_vinyl(
        vinyl: VinylDTO,
        vinyl_service: Annotated[VinylService, Depends(VinylService)],
) -> VinylDTO:
    return await vinyl_service.add_vinyl(vinyl)


@vinyl_router.get('', response_model=VinylDTO)
async def get_vinyl_by_id(
        vinyl_id: int,
        vinyl_service: Annotated[VinylService, Depends(VinylService)],
) -> VinylDTO:
    return await vinyl_service.get_vinyl_by_id(vinyl_id)


@vinyl_router.put('', response_model=VinylDTO)
async def update_vinyl(
        vinyl_id: int,
        new_vinyl: VinylDTO,
        vinyl_service: Annotated[VinylService, Depends(VinylService)],
) -> VinylDTO:
    return await vinyl_service.update_vinyl(vinyl_id, new_vinyl)

@vinyl_router.delete('', response_model=str)
async def delete_vinyl(
        vinyl_id: int,
        vinyl_service: Annotated[VinylService, Depends(VinylService)],
) -> str:
    return await vinyl_service.delete_vinyl(vinyl_id)