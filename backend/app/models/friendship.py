import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base


class FriendshipStatus:
    PENDING = "pending"
    ACCEPTED = "accepted"
    BLOCKED = "blocked"


class Friendship(Base):
    __tablename__ = "friendships"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    initiator_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), index=True)
    receiver_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), index=True)
    status: Mapped[str] = mapped_column(String(20), default=FriendshipStatus.PENDING)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    initiator: Mapped["User"] = relationship("User", foreign_keys=[initiator_id], back_populates="friendships_initiated")  # noqa: F821, E501
    receiver: Mapped["User"] = relationship("User", foreign_keys=[receiver_id], back_populates="friendships_received")  # noqa: F821, E501
