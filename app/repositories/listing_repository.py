from sqlalchemy.orm import Session
from app.models.user import User
from app.models.listing import Listing
from geopy.distance import geodesic
from fastapi import HTTPException
from app.models.booking import Booking
from app.models.enums import BookingStatus

def create_listing(
    db: Session,
    listing: Listing
):
    db.add(listing)

    db.commit()

    db.refresh(listing)

    return listing

def get_all_listings(db: Session):

    listings = db.query(Listing).all()

    for listing in listings:

        owner = (
            db.query(User)
            .filter(User.id == listing.owner_id)
            .first()
        )

        listing.owner_name = owner.full_name if owner else ""

    return listings


def get_listing_by_id(
    db: Session,
    listing_id: int
):

    listing = (
        db.query(Listing)
        .filter(Listing.id == listing_id)
        .first()
    )

    if listing:

        owner = (
            db.query(User)
            .filter(User.id == listing.owner_id)
            .first()
        )

        listing.owner_name = owner.full_name if owner else ""

    return listing

def get_my_listings(
    db: Session,
    owner_id: int
):

    listings = (
        db.query(Listing)
        .filter(Listing.owner_id == owner_id)
        .all()
    )

    for listing in listings:
        listing.owner_name = (
            db.query(User)
            .filter(User.id == listing.owner_id)
            .first()
            .full_name
        )

    return listings

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
    bookings = (
        db.query(Booking)
        .filter(
            Booking.listing_id == listing.id
        )
        .all()
    )

    # If any booking is not completed, block deletion
    for booking in bookings:
        if booking.status != BookingStatus.COMPLETED:
            raise HTTPException(
                status_code=400,
                detail="Cannot delete listing because it has active or pending bookings."
            )

    # All bookings are completed, delete them first
    for booking in bookings:
        db.delete(booking)

    # Now delete the listing
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
    "owner_id": listing.owner_id,
    "title": listing.title,
    "address": listing.address,
    "latitude": listing.latitude,
    "longitude": listing.longitude,
    "hourly_rate": listing.hourly_rate,
    "total_spaces": listing.total_spaces,
    "available_spaces": listing.available_spaces,
    "description": listing.description,
    "image_url": listing.image_url,
    "amenities": listing.amenities,
    "is_active": listing.is_active,
    "distance_km": round(distance, 2),
    "owner_name": (
         db.query(User)
         .filter(User.id == listing.owner_id)
         .first()
         .full_name
         ),
})

    nearby.sort(
        key=lambda x: x["distance_km"]
    )

    return nearby