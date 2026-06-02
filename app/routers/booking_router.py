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
    check_in_booking,
    request_exit_booking,
    confirm_exit_booking
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

    listing.available_spaces -= 1


    booking = Booking(
        user_id=current_user.id,
        listing_id=listing.id,
        start_time=booking_data.start_time,
        end_time=booking_data.end_time,
        total_cost=total_cost,
        status=BookingStatus.CONFIRMED.value
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

    return get_my_bookings(
        db,
        current_user.id
    )


@router.post(
    "/{booking_id}/check-in",
    response_model=BookingResponse
)

def check_in(
    booking_id: int,
    db: Session = Depends(get_db)
):
    booking = get_booking_by_id(
        db,
        booking_id
    )

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    if booking.status != BookingStatus.CONFIRMED:
        raise HTTPException(
            status_code=400,
            detail="Booking must be CONFIRMED"
        )

    return check_in_booking(
        db,
        booking
    )

@router.post(
    "/{booking_id}/request-exit",
    response_model=BookingResponse
)
def request_exit(
    booking_id: int,
    db: Session = Depends(get_db)
):
    booking = get_booking_by_id(
        db,
        booking_id
    )

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    if booking.status != BookingStatus.ACTIVE:
        raise HTTPException(
            status_code=400,
            detail="Booking must be ACTIVE"
        )

    return request_exit_booking(
        db,
        booking
    )

@router.post(
    "/{booking_id}/confirm-exit",
    response_model=BookingResponse
)
def confirm_exit(
    booking_id: int,
    db: Session = Depends(get_db)
):
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