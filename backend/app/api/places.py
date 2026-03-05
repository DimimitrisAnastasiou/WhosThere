from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from app.db.session import get_db
from app.middleware.auth import get_current_user
from app.models.place import Place
from app.models.user import User
from app.schemas.place import PlaceCreate, PlaceResponse, PlaceSearchResult
from app.services.place_service import search_google_places

router = APIRouter()


@router.get("/search", response_model=list[PlaceSearchResult])
async def search_places(
    q: str = Query(..., min_length=2, description="Search query"),
):
    """
    Search Google Places API for real-world locations.
    Returns results before they are saved to our DB.
    """
    return await search_google_places(q)


@router.get("", response_model=list[PlaceResponse])
async def list_places(
    q: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    """List places already in our DB. Supports name search."""
    query = select(Place).order_by(Place.name)
    if q:
        query = query.where(Place.name.ilike(f"%{q}%"))

    result = await db.execute(query)
    return result.scalars().all()


@router.post("", response_model=PlaceResponse, status_code=201)
async def create_place(
    body: PlaceCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Upsert a place into our DB.
    Called when a user selects a Google result or creates a custom place.
    """
    # Avoid duplicates by google_place_id
    if body.google_place_id:
        result = await db.execute(
            select(Place).where(Place.google_place_id == body.google_place_id)
        )
        existing = result.scalar_one_or_none()
        if existing:
            return existing

    place = Place(
        **body.model_dump(),
        created_by=current_user.id,
    )
    db.add(place)
    await db.flush()
    await db.refresh(place)
    return place


@router.get("/{place_id}", response_model=PlaceResponse)
async def get_place(place_id: str, db: AsyncSession = Depends(get_db)):
    place = await db.get(Place, place_id)
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    return place
