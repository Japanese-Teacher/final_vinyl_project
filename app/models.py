from pydantic import BaseModel

class VinylDTO(BaseModel):
    album_name: str
    artist: str
    producer: str
    cost: int
    description: str | None