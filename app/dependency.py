from fastapi import Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.settings import Settings
from app.streaming.service import VideoService
from app.streaming.repository.cache_video import VideoCache
from app.streaming.repository.video import VideoRepository
from app.infrastructure.cache import get_redis_connection
from app.infrastructure.database import get_db_session


async def get_video_repository(db_session: AsyncSession = Depends(get_db_session)) -> VideoRepository:
    return VideoRepository(
        settings=Settings(),
        db_session=db_session
    )


async def get_video_cache_repository() -> VideoCache:
    redis_connection = get_redis_connection()
    return VideoCache(
        redis_connection,
        settings=Settings(),
    )


async def get_video_service(
        background_tasks: BackgroundTasks,
        video_repository: VideoRepository = Depends(get_video_repository),
        video_cache: VideoCache = Depends(get_video_cache_repository),

) -> VideoService:
    return VideoService(
        video_repository=video_repository,
        video_cache=video_cache,
        settings=Settings(),
        background_tasks=background_tasks
    )
