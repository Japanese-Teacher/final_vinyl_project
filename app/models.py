from pydantic import BaseModel

class VynilDTO(BaseModel):
    id: int
    album_name: str
    artist: str
    producer: str
