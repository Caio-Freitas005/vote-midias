from pydantic import BaseModel

class MediaCreate(BaseModel):
    title: str
    genre: str
    description: str | None = None
    image: str 