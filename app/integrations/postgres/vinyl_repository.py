from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import VinylDTO, VinylResponse
from app.orm import VinylORM
from app.transport.depends.db import get_async_session


class VinylRepository:
    def __init__(
            self,
            async_session: Annotated[AsyncSession, Depends(get_async_session)]
    ):
        self.async_session = async_session

    async def vinyl_exists(self, album_name: str, artist: str) -> bool:
        vinyl_result = await self.async_session.execute(
            select(VinylORM)
            .where(
                VinylORM.album_name == album_name and
                VinylORM.artist == artist
            )
        )
        vinyl_orm = vinyl_result.scalar_one_or_none()
        if not vinyl_orm:
            return False
        return True

    async def vinyl_by_id_exists(self, vinyl_id: int) -> bool:
        vinyl_result = await self.async_session.execute(
            select(VinylORM)
            .where(VinylORM.id == vinyl_id)
        )
        vinyl_orm = vinyl_result.scalar_one_or_none()
        if not vinyl_orm:
            return False
        return True

    async def add_vinyl(self, vinyl: VinylDTO) -> VinylResponse:
        vinyl_orm = VinylORM(
            artist=vinyl.artist,
            album_name=vinyl.album_name,
            producer=vinyl.producer,
            cost=vinyl.cost,
            description=vinyl.description,
        )
        self.async_session.add(vinyl_orm)
        await self.async_session.flush()
        await self.async_session.refresh(vinyl_orm)
        return VinylResponse(
            id=vinyl_orm.id,
            artist=vinyl_orm.artist,
            album_name=vinyl_orm.album_name,
            producer=vinyl_orm.producer,
            cost=vinyl_orm.cost,
            description=vinyl_orm.description,
        )

    async def get_vinyl_by_id(self, vinyl_id: int) -> VinylResponse:
        vinyl_obj = await self.async_session.execute(select(VinylORM).where(VinylORM.id == vinyl_id))
        vinyl_orm = vinyl_obj.scalars().first()
        if not vinyl_orm:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vinyl with id {vinyl_id} not found"
            )
        vinyl_dto = VinylResponse(
            id=vinyl_orm.id,
            album_name=vinyl_orm.album_name,
            artist=vinyl_orm.artist,
            producer=vinyl_orm.producer,
            cost=vinyl_orm.cost,
            description=vinyl_orm.description,
        )
        return vinyl_dto

    async def update_vinyl(
            self,
            vinyl_id: int,
            new_vinyl: VinylDTO
    ) -> VinylResponse:
        vinyl_orm = await self.async_session.get(VinylORM, vinyl_id)
        if vinyl_orm:
            vinyl_orm.album_name = new_vinyl.album_name
            vinyl_orm.artist = new_vinyl.artist
            vinyl_orm.producer = new_vinyl.producer
            vinyl_orm.cost = new_vinyl.cost
            vinyl_orm.description = new_vinyl.description
            await self.async_session.flush()
            await self.async_session.refresh(vinyl_orm)
        return VinylResponse(
            id=vinyl_orm.id,
            artist=vinyl_orm.artist,
            album_name=vinyl_orm.album_name,
            producer=vinyl_orm.producer,
            cost=vinyl_orm.cost,
            description=vinyl_orm.description,
        )

    async def delete_vinyl(self, vinyl_id: int) -> str:
        result = await self.async_session.execute(
            select(VinylORM).where(VinylORM.id == vinyl_id)
        )
        vinyl_orm = result.scalars().first()

        if not vinyl_orm:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vinyl with id {vinyl_id} not found"
            )
        await self.async_session.execute(delete(VinylORM).where(VinylORM.id == vinyl_id))
        await self.async_session.flush()
        return "Удаление успешно произведено"
