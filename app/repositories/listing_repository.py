from sqlalchemy.orm import Session

from app.models.listing import Listing


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