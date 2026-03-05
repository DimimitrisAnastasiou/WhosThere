from datetime import datetime
from pydantic import BaseModel


class UserCreate(BaseModel):
    supabase_id: str
    username: str | None = None
    display_name: str | None = None
    avatar_url: str | None = None
    is_anonymous: bool = False


class UserUpdate(BaseModel):
    username: str | None = None
    display_name: str | None = None
    avatar_url: str | None = None


class UserResponse(BaseModel):
    id: str
    username: str | None
    display_name: str | None
    avatar_url: str | None
    is_anonymous: bool
    created_at: datetime

    model_config = {"from_attributes": True}
