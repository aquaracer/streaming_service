import os
import logging
from dataclasses import dataclass
from fastapi import BackgroundTasks
from typing import Optional

from app.exception import VideoNotFound
from app.settings import Settings
from app.streaming.models import Video
from app.streaming.repository.cache_video import VideoCache
from app.streaming.repository.video import VideoRepository
from app.streaming.schema import VideoSchema, VideoCreateSchema

logger = logging.getLogger(__name__)


@dataclass
class VideoService:
    background_tasks: BackgroundTasks
    video_repository: VideoRepository
    video_cache: VideoCache
    settings: Settings

    async def add_video(self, body: VideoCreateSchema) -> VideoSchema:
        video: Video = await self.video_repository.add_video(body=body)
        video_schema: VideoSchema = VideoSchema.model_validate(video)
        self.background_tasks.add_task(self.handle_uploaded_video, video_schema)
        return video_schema

    async def get_video(self, video_id: int) -> VideoSchema:
        if cached_video := await self.video_cache.get_cached_video(video_id=video_id):
            return cached_video
        else:
            video: Video | None = await self.video_repository.get_video(video_id=video_id)
            if not video:
                raise VideoNotFound
            video_schema = VideoSchema.model_validate(video)
            await self.video_cache.set_cached_video(video_schema=video_schema)
            return video_schema

    async def handle_uploaded_video(self, video_schema: VideoSchema) -> None:
        logger.info(f"Starting video processing for video ID: {video_schema.id}")
        try:
            playlist_path = self._generate_hls_playlist(video_schema.id)
            logger.info(f"HLS playlist generated successfully at: {playlist_path}")
            await self.video_cache.set_cached_video(video_schema=video_schema)
            logger.debug(f"Video {video_schema.id} cached successfully")
        except Exception as error:
            logger.error(f"Failed to process video {video_schema.id}: {str(error)}", exc_info=True)
            raise

    def _generate_hls_playlist(self, video_id: int) -> str:
        logger.debug(f"Generating HLS playlist for video ID: {video_id}")
        try:
            hls_content = f"""#EXTM3U
            #EXT-X-VERSION:3
            #EXT-X-MEDIA-SEQUENCE:0
            #EXT-X-TARGETDURATION:10

            #EXTINF:10.0,
            segment1.ts
            #EXTINF:10.0,
            segment2.ts
            #EXTINF:10.0,
            segment3.ts
            #EXT-X-ENDLIST
            """
            playlist_path = f"media/hls/{video_id}.m3u8"
            os.makedirs("media/hls", exist_ok=True)

            with open(playlist_path, "w") as file:
                file.write(hls_content)

            logger.debug(f"HLS playlist file created at: {playlist_path}")
            return playlist_path
        except Exception as error:
            logger.error(f"Failed to generate HLS playlist for video {video_id}: {str(error)}", exc_info=True)
            raise
