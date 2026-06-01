from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from sqlalchemy.orm import Session
from app.repositories.listing_repository import (
    create_listing,
    get_all_listings,
    get_listing_by_id,
    get_my_listings,
    update_listing,
    delete_listing
)
from app.schemas.listing import (
    ListingCreate,
    ListingResponse,
    ListingUpdate
)


from app.database import get_db

from app.models.listing import Listing

from app.core.dependencies import get_current_user




router = APIRouter(
    prefix="/listings",
    tags=["Listings"]
)


@router.post(
    "/",
    response_model=ListingResponse
)
def create_new_listing(
    listing: ListingCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    new_listing = Listing(
        owner_id=current_user.id,

        title=listing.title,
        address=listing.address,

        latitude=listing.latitude,
        longitude=listing.longitude,

        hourly_rate=listing.hourly_rate,

        total_spaces=listing.total_spaces,

        available_spaces=listing.total_spaces,

        description=listing.description
    )

    return create_listing(
        db,
        new_listing
    )

@router.get(
    "/",
    response_model=list[ListingResponse]
)
def get_listings(
    db: Session = Depends(get_db)
):
    return get_all_listings(db)

@router.get(
    "/my",
    response_model=list[ListingResponse]
)
def get_current_user_listings(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return get_my_listings(
        db,
        current_user.id
    )


@router.get(
    "/{listing_id}",
    response_model=ListingResponse
)
def get_listing(
    listing_id: int,
    db: Session = Depends(get_db)
):

    listing = get_listing_by_id(
        db,
        listing_id
    )

    if not listing:
        raise HTTPException(
            status_code=404,
            detail="Listing not found"
        )

    return listing

@router.patch(
    "/{listing_id}",
    response_model=ListingResponse
)
def update_existing_listing(
    listing_id: int,
    listing_data: ListingUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    listing = get_listing_by_id(
        db,
        listing_id
    )

    if not listing:
        raise HTTPException(
            status_code=404,
            detail="Listing not found"
        )

    if listing.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    update_data = listing_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(
            listing,
            field,
            value
        )

    return update_listing(
        db,
        listing
    )

@router.delete("/{listing_id}")
def remove_listing(
    listing_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    listing = get_listing_by_id(
        db,
        listing_id
    )

    if not listing:
        raise HTTPException(
            status_code=404,
            detail="Listing not found"
        )

    if listing.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    delete_listing(
        db,
        listing
    )

    return {
        "message": "Listing deleted successfully"
    }