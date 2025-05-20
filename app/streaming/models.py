from app.infrastructure.database import Base
from sqlalchemy.orm import Mapped, mapped_column


class Video(Base):
    __tablename__ = "videos"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(nullable=False)
    playlist_url: Mapped[str] = mapped_column(nullable=True)
