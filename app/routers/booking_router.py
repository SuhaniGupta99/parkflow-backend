from datetime import datetime

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.booking import (
    BookingCreate,
    BookingResponse
)
from app.models.booking import Booking
from app.models.enums import BookingStatus

from app.repositories.booking_repository import (
    create_booking,
    get_my_bookings,
    get_booking_by_id,
    confirm_exit_booking,
    approve_booking,
    reject_booking,
    get_pending_bookings_for_host
)

from app.repositories.listing_repository import (
    get_listing_by_id
)

from app.core.dependencies import (
    get_current_user
)

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)

@router.post(
    "/",
    response_model=BookingResponse
)
def create_new_booking(
    booking_data: BookingCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.role != "CUSTOMER":
        raise HTTPException(
            status_code=403,
            detail="Only customers can create bookings"
        )

    listing = get_listing_by_id(
        db,
        booking_data.listing_id
    )

    if not listing:
        raise HTTPException(
            status_code=404,
            detail="Listing not found"
        )

    if listing.available_spaces <= 0:
        raise HTTPException(
            status_code=400,
            detail="No spaces available"
        )

    duration_hours = (
        booking_data.end_time -
        booking_data.start_time
    ).total_seconds() / 3600

    if duration_hours <= 0:
        raise HTTPException(
            status_code=400,
            detail="Invalid booking duration"
        )

    total_cost = (
        duration_hours *
        listing.hourly_rate
    )



    booking = Booking(
        user_id=current_user.id,
        listing_id=listing.id,
        start_time=booking_data.start_time,
        end_time=booking_data.end_time,
        total_cost=total_cost,
        status=BookingStatus.PENDING.value
    )

    db.add(booking)
    db.commit()

    db.refresh(booking)

    return booking


@router.get(
    "/my",
    response_model=list[BookingResponse]
)
def get_current_user_bookings(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.role != "CUSTOMER":
        raise HTTPException(
            status_code=403,
            detail="Only customers have bookings"
        )

    return get_my_bookings(
        db,
        current_user.id
    )

@router.get("/pending")
def get_pending_requests(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.role != "HOST":
        raise HTTPException(
            status_code=403,
            detail="Only hosts can view booking requests"
        )

    return get_pending_bookings_for_host(
        db,
        current_user.id
    )
@router.post("/{booking_id}/approve")
def approve_booking_request(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.role != "HOST":
        raise HTTPException(
            status_code=403,
            detail="Only hosts can approve bookings"
        )

    booking = get_booking_by_id(
        db,
        booking_id
    )

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    listing = get_listing_by_id(
        db,
        booking.listing_id
    )

    if listing.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    if booking.status != BookingStatus.PENDING:
        raise HTTPException(
            status_code=400,
            detail="Booking must be PENDING"
        )
    if listing.available_spaces <= 0:
        raise HTTPException(
            status_code=400,
            detail="No spaces available"
        )
    
    listing.available_spaces -= 1
    
    db.commit()
    
    return approve_booking(
        db,
        booking
    )

@router.post("/{booking_id}/reject")
def reject_booking_request(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.role != "HOST":
        raise HTTPException(
            status_code=403,
            detail="Only hosts can reject bookings"
        )

    booking = get_booking_by_id(
        db,
        booking_id
    )

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    listing = get_listing_by_id(
        db,
        booking.listing_id
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

    if booking.status != BookingStatus.PENDING:
        raise HTTPException(
            status_code=400,
            detail="Booking must be PENDING"
        )

    return reject_booking(
        db,
        booking
    )


@router.post(
    "/{booking_id}/confirm-exit",
    response_model=BookingResponse
)
def confirm_exit(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.role != "HOST":
        raise HTTPException(
            status_code=403,
            detail="Only hosts can confirm exits"
        )
    
    booking = get_booking_by_id(
        db,
        booking_id
    )

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    if booking.status != BookingStatus.EXIT_REQUESTED:
        raise HTTPException(
            status_code=400,
            detail="Booking must be EXIT_REQUESTED"
        )

    listing = get_listing_by_id(
        db,
        booking.listing_id
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

    duration = (
        datetime.utcnow()
        - booking.actual_start_time
    )

    hours = duration.total_seconds() / 3600

    final_cost = (
        hours *
        listing.hourly_rate
    )

    listing.available_spaces += 1

    db.commit()

    return confirm_exit_booking(
        db,
        booking,
        final_cost
    )