import uuid
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base


class CheckIn(Base):
    __tablename__ = "checkins"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), index=True)
    place_id: Mapped[str] = mapped_column(String, ForeignKey("places.id"), index=True)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_anonymous: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    duration_minutes: Mapped[int | None] = mapped_column(nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="checkins")  # noqa: F821
    place: Mapped["Place"] = relationship("Place", back_populates="checkins")  # noqa: F821
