from typing import Optional

from sqlalchemy import String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class VinylORM(Base):
    def __repr__(self):
        return (f"VinylORM("
                f"id = {self.id}, "
                f"album_name = {self.album_name}, "
                f"artist = {self.artist}, "
                f"cost = {self.cost}")
    __tablename__ = "vinyl records"
    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        autoincrement=True,
    )
    artist: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    album_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    producer: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    cost: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str | None] = mapped_column(Text, default=None)

