import uuid
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    supabase_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(50), unique=True, nullable=True)
    display_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String, nullable=True)
    is_anonymous: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    checkins: Mapped[list["CheckIn"]] = relationship("CheckIn", back_populates="user")  # noqa: F821
    friendships_initiated: Mapped[list["Friendship"]] = relationship(  # noqa: F821
        "Friendship", foreign_keys="Friendship.initiator_id", back_populates="initiator"
    )
    friendships_received: Mapped[list["Friendship"]] = relationship(  # noqa: F821
        "Friendship", foreign_keys="Friendship.receiver_id", back_populates="receiver"
    )
