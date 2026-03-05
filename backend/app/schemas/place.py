from datetime import datetime
from pydantic import BaseModel


class PlaceCreate(BaseModel):
    name: str
    google_place_id: str | None = None
    address: str | None = None
    lat: float | None = None
    lng: float | None = None
    is_custom: bool = False


class PlaceResponse(BaseModel):
    id: str
    name: str
    google_place_id: str | None
    address: str | None
    lat: float | None
    lng: float | None
    is_custom: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class PlaceSearchResult(BaseModel):
    """Returned from Google Places search before saving to DB."""
    google_place_id: str
    name: str
    address: str
    lat: float
    lng: float
