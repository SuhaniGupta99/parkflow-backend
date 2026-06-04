from sqlalchemy.orm import Session

from app.models.listing import Listing
from geopy.distance import geodesic

def create_listing(
    db: Session,
    listing: Listing
):
    db.add(listing)

    db.commit()

    db.refresh(listing)

    return listing

def get_all_listings(db: Session):
    return db.query(Listing).all()


def get_listing_by_id(
    db: Session,
    listing_id: int
):
    return (
        db.query(Listing)
        .filter(Listing.id == listing_id)
        .first()
    )

def get_my_listings(
    db: Session,
    owner_id: int
):
    return (
        db.query(Listing)
        .filter(
            Listing.owner_id == owner_id
        )
        .all()
    )

def update_listing(
    db: Session,
    listing: Listing
):
    db.commit()
    db.refresh(listing)
    return listing


def delete_listing(
    db: Session,
    listing: Listing
):
    db.delete(listing)
    db.commit()

def get_nearby_listings(
    db: Session,
    latitude: float,
    longitude: float,
    radius_km: float
):
    listings = (
        db.query(Listing)
        .filter(
            Listing.is_active == True,
            Listing.available_spaces > 0
        )
        .all()
    )

    nearby = []

    for listing in listings:

        distance = geodesic(
            (latitude, longitude),
            (listing.latitude, listing.longitude)
        ).km

        if distance <= radius_km:

            nearby.append({
                "id": listing.id,
                "title": listing.title,
                "address": listing.address,
                "latitude": listing.latitude,
                "longitude": listing.longitude,
                "hourly_rate": listing.hourly_rate,
                "available_spaces": listing.available_spaces,
                "distance_km": round(distance, 2)
            })

    nearby.sort(
        key=lambda x: x["distance_km"]
    )

    return nearby