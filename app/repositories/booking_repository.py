from sqlalchemy.orm import Session

from app.models.booking import Booking
from datetime import datetime

def create_booking(
    db: Session,
    booking: Booking
):
    db.add(booking)

    db.commit()

    db.refresh(booking)

    return booking


def get_my_bookings(
    db: Session,
    user_id: int
):
    return (
        db.query(Booking)
        .filter(
            Booking.user_id == user_id
        )
        .all()
    )

def check_in_booking(
    db: Session,
    booking: Booking
):
    booking.status = "ACTIVE"
    booking.actual_start_time = datetime.utcnow()

    db.commit()
    db.refresh(booking)

    return booking

def request_exit_booking(
    db: Session,
    booking: Booking
):
    booking.status = "EXIT_REQUESTED"
    booking.exit_requested_at = datetime.utcnow()

    db.commit()
    db.refresh(booking)

    return booking


def confirm_exit_booking(
    db: Session,
    booking: Booking,
    final_cost: float
):
    booking.status = "COMPLETED"

    booking.actual_end_time = datetime.utcnow()

    booking.total_cost = final_cost

    db.commit()
    db.refresh(booking)

    return booking

def get_booking_by_id(
    db: Session,
    booking_id: int
):
    return (
        db.query(Booking)
        .filter(
            Booking.id == booking_id
        )
        .first()
    )