import json
from dataclasses import dataclass
from redis import asyncio as Redis

from app.settings import Settings
from app.streaming.schema import VideoSchema


@dataclass
class VideoCache:
    redis: Redis
    settings: Settings

    async def get_cached_video(self, video_id: int) -> VideoSchema:
        async with self.redis as redis:
            if video := await redis.get(f"video:{video_id}"):
                return VideoSchema.model_validate(json.loads(video))
            else:
                return []

    async def set_cached_video(self, video_schema: VideoSchema) -> None:
        async with self.redis as redis:
            await redis.set(
                f"video:{video_schema.id}",
                video_schema.model_dump_json(),
                ex=self.settings.CACHE_TTL_SECONDS
            )
