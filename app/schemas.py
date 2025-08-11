from pydantic import BaseModel, HttpUrl

class MediaCreate(BaseModel):
    title: str
    genre: str
    description: str | None = None
    image: HttpUrl

class MediaUpdate(BaseModel):
    title: str
    genre: str
    description: str | None = None
    image: HttpUrl