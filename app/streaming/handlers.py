from typing import Annotated
from fastapi import APIRouter, status, Depends, HTTPException

from app.dependency import get_video_service
from app.exception import VideoNotFound

from app.streaming.schema import VideoSchema, VideoCreateSchema
from app.streaming.service import VideoService

router = APIRouter(prefix='/api/videos', tags=['videos'])


@router.post("", response_model=VideoSchema, status_code=status.HTTP_201_CREATED)
async def add_video(
        body: VideoCreateSchema,
        video_service: Annotated[VideoService, Depends(get_video_service)]
):
    return await video_service.add_video(body=body)


@router.get("/{id}", response_model=VideoSchema)
async def get_video(
        id: int,
        video_service: Annotated[VideoService, Depends(get_video_service)]
):
    try:
        return await video_service.get_video(video_id=id)
    except VideoNotFound as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error.detail
        )
