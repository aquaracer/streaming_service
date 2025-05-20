from dataclasses import dataclass

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.settings import Settings
from app.streaming.models import Video
from app.streaming.schema import VideoCreateSchema


@dataclass
class VideoRepository:
    db_session: AsyncSession
    settings: Settings

    async def add_video(self, body: VideoCreateSchema) -> Video | None:
        query = insert(Video).values(title=body.title, url=body.url).returning(Video.id)
        async with self.db_session as session:
            video_id: int = (await session.execute(query)).scalar()
            await session.commit()
            await session.flush()
            query = update(Video).where(Video.id == video_id).values(
                playlist_url=f"{self.settings.HLS_HOST_URL}{video_id}.m3u8"
                )
            await session.execute(query)
            await session.commit()
            await session.flush()
            return await self.get_video(video_id)

    async def get_video(self, video_id: int) -> Video | None:
        query = select(Video).where(Video.id == video_id)
        async with self.db_session as session:
            return (await session.execute(query)).scalar_one_or_none()
