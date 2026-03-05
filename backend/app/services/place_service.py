import httpx
from app.config import get_settings

settings = get_settings()

PLACES_BASE = "https://maps.googleapis.com/maps/api/place"


async def search_google_places(query: str) -> list[dict]:
    """
    Search Google Places Text Search API.
    Returns a list of place candidates.
    """
    params = {
        "query": query,
        "key": settings.google_places_api_key,
        "fields": "place_id,name,formatted_address,geometry",
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{PLACES_BASE}/textsearch/json", params=params)
        resp.raise_for_status()
        data = resp.json()

    results = []
    for r in data.get("results", [])[:8]:
        loc = r.get("geometry", {}).get("location", {})
        results.append({
            "google_place_id": r.get("place_id"),
            "name": r.get("name"),
            "address": r.get("formatted_address"),
            "lat": loc.get("lat"),
            "lng": loc.get("lng"),
        })
    return results
