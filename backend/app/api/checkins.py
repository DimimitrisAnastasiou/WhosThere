from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.middleware.auth import get_current_user, get_optional_user
from app.models.checkin import CheckIn
from app.models.place import Place
from app.models.user import User
from app.schemas.checkin import CheckInCreate, CheckInResponse

router = APIRouter()


@router.post("", response_model=CheckInResponse, status_code=status.HTTP_201_CREATED)
async def create_checkin(
    body: CheckInCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Check in to a place. Requires authentication."""
    place = await db.get(Place, body.place_id)
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    checkin = CheckIn(
        user_id=current_user.id,
        place_id=body.place_id,
        note=body.note,
        is_anonymous=body.is_anonymous,
        duration_minutes=body.duration_minutes,
    )
    db.add(checkin)
    await db.flush()

    # Reload with relationships for response
    result = await db.execute(
        select(CheckIn)
        .where(CheckIn.id == checkin.id)
        .options(selectinload(CheckIn.user), selectinload(CheckIn.place))
    )
    return result.scalar_one()


@router.get("", response_model=list[CheckInResponse])
async def list_checkins(
    limit: int = Query(default=20, le=100),
    offset: int = Query(default=0, ge=0),
    place_id: str | None = Query(default=None),
    _: User | None = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """List recent check-ins. Optionally filter by place."""
    query = (
        select(CheckIn)
        .options(selectinload(CheckIn.user), selectinload(CheckIn.place))
        .order_by(desc(CheckIn.created_at))
        .limit(limit)
        .offset(offset)
    )
    if place_id:
        query = query.where(CheckIn.place_id == place_id)

    result = await db.execute(query)
    return result.scalars().all()


@router.delete("/{checkin_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_checkin(
    checkin_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete your own check-in."""
    checkin = await db.get(CheckIn, checkin_id)
    if not checkin:
        raise HTTPException(status_code=404, detail="CheckIn not found")
    if checkin.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your check-in")

    await db.delete(checkin)
