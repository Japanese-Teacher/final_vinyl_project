from typing import Annotated

from fastapi import Depends
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import VinylDTO
from app.orm import VinylORM
from app.transport.depends.db import get_async_session


class VinylRepository:
    def __init__(
            self,
            async_session: Annotated[AsyncSession, Depends(get_async_session)]
    ):
        self.async_session = async_session

    async def add_vinyl(self, vinyl: VinylDTO) -> VinylDTO:
        self.async_session.add(
            VinylORM(
                artist=vinyl.artist,
                album_name=vinyl.album_name,
                producer=vinyl.producer,
                cost=vinyl.cost,
                description=vinyl.description,
            )
        )
        await self.async_session.flush()
        return vinyl

    async def get_vinyl_by_id(self, vinyl_id: int) -> VinylDTO:
        vinyl_obj = await self.async_session.execute(select(VinylORM).where(VinylORM.id == vinyl_id))
        vinyl_orm = vinyl_obj.scalars().first()
        vinyl_dto = VinylDTO(
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
    ) -> VinylDTO:
        vinyl = await self.async_session.get(VinylORM, vinyl_id)
        if vinyl:
            vinyl.album_name = new_vinyl.album_name
            vinyl.artist = new_vinyl.artist
            vinyl.producer = new_vinyl.producer
            vinyl.cost = new_vinyl.cost
            vinyl.description = new_vinyl.description
            await self.async_session.flush()
            await self.async_session.refresh(vinyl)
        return new_vinyl

    async def delete_vinyl(self, vinyl_id: int) -> str:
        await self.async_session.execute(delete(VinylORM).where(VinylORM.id == vinyl_id))
        await self.async_session.flush()
        return "Удаление успешно произведено"