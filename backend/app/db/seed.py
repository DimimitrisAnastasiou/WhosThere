"""
Seed the database with sample data for local development.
Usage: make seed
"""
import asyncio
import uuid
from app.db.session import AsyncSessionLocal
from app.models.user import User
from app.models.place import Place
from app.models.checkin import CheckIn


async def seed():
    async with AsyncSessionLocal() as db:
        # Sample users
        alice = User(
            id=str(uuid.uuid4()),
            supabase_id="seed-alice",
            username="alice",
            display_name="Alice",
            is_anonymous=False,
        )
        bob = User(
            id=str(uuid.uuid4()),
            supabase_id="seed-bob",
            username="bob",
            display_name="Bob",
            is_anonymous=False,
        )
        db.add_all([alice, bob])
        await db.flush()

        # Sample places
        cafe = Place(
            id=str(uuid.uuid4()),
            name="The Great Café",
            address="123 Main St",
            lat=40.7128,
            lng=-74.0060,
            is_custom=True,
            created_by=alice.id,
        )
        gym = Place(
            id=str(uuid.uuid4()),
            name="Iron Gym",
            address="456 Park Ave",
            lat=40.7138,
            lng=-74.0070,
            is_custom=True,
            created_by=bob.id,
        )
        db.add_all([cafe, gym])
        await db.flush()

        # Sample check-ins
        db.add_all([
            CheckIn(id=str(uuid.uuid4()), user_id=alice.id, place_id=cafe.id, note="Great coffee!"),
            CheckIn(id=str(uuid.uuid4()), user_id=bob.id, place_id=gym.id, note="Leg day 🦵"),
        ])

        await db.commit()
        print("✅ Seed complete")


if __name__ == "__main__":
    asyncio.run(seed())
