from datetime import datetime
from pydantic import BaseModel


class CheckInCreate(BaseModel):
    place_id: str
    note: str | None = None
    is_anonymous: bool = False


class PlaceSnippet(BaseModel):
    id: str
    name: str
    address: str | None

    model_config = {"from_attributes": True}


class UserSnippet(BaseModel):
    id: str
    display_name: str | None
    avatar_url: str | None
    is_anonymous: bool

    model_config = {"from_attributes": True}


class CheckInResponse(BaseModel):
    id: str
    note: str | None
    is_anonymous: bool
    created_at: datetime
    place: PlaceSnippet
    user: UserSnippet

    model_config = {"from_attributes": True}
