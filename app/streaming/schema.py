import os
from urllib.parse import urlparse

from pydantic import BaseModel, field_validator


class VideoSchema(BaseModel):
    id: int
    title: str
    playlist_url: str | None = None

    class Config:
        from_attributes = True


class VideoCreateSchema(BaseModel):
    title: str
    url: str

    @field_validator('url')
    @classmethod
    def url_must_be_video_file(cls, url: str) -> str:
        result = urlparse(url)
        if result.scheme not in ["http", "https"] or not result.path:
            raise ValueError('Invalid URL Format')

        filename = os.path.basename(result.path)
        if not filename:
            raise ValueError('Invalid URL Format')

        extension = os.path.splitext(filename)[1]
        if not extension:
            raise ValueError('Url Does Not Contain File')

        if extension not in [".mp4", ".mov", ".avi", ".wmv", ".mkv", ".flv"]:
            raise ValueError('Incorrect File Type')

        return url
