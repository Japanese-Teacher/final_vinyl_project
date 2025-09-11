from typing import Annotated, Optional

from fastapi import APIRouter, Depends

from app.models import VinylDTO, VinylResponse
from app.services.vinyl_service import VinylService

vinyl_router = APIRouter(
    prefix='/vinyls',
    tags=["Vinyls"]
)


@vinyl_router.post('', response_model=VinylResponse)
async def add_vinyl(
        vinyl: VinylDTO,
        vinyl_service: Annotated[VinylService, Depends(VinylService)],
) -> VinylResponse:
    return await vinyl_service.add_vinyl(vinyl)


@vinyl_router.get('/{vinyl_id}', response_model=VinylResponse)
async def get_vinyl_by_id(
        vinyl_id: int,
        vinyl_service: Annotated[VinylService, Depends(VinylService)],
) -> VinylResponse:
    return await vinyl_service.get_vinyl_by_id(vinyl_id)


@vinyl_router.get('', response_model=Optional[list[VinylResponse]])
async def get_all_vinyl(
        page: int,
        size: int,
        vinyl_service: Annotated[VinylService, Depends(VinylService)],
) -> Optional[list[VinylResponse]]:
    return await vinyl_service.get_all_vinyl(page, size)


@vinyl_router.put('/{vinyl_id}', response_model=VinylResponse)
async def update_vinyl(
        vinyl_id: int,
        new_vinyl: VinylDTO,
        vinyl_service: Annotated[VinylService, Depends(VinylService)],
) -> VinylResponse:
    return await vinyl_service.update_vinyl(vinyl_id, new_vinyl)


@vinyl_router.delete('/{vinyl_id}', response_model=str)
async def delete_vinyl(
        vinyl_id: int,
        vinyl_service: Annotated[VinylService, Depends(VinylService)],
) -> str:
    return await vinyl_service.delete_vinyl(vinyl_id)
