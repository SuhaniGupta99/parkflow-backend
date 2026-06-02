from sqlalchemy import (
    Column,
    Integer,
    Float,
    ForeignKey,
    DateTime,
    String,
    Enum
)


from app.database import Base
from app.models.enums import BookingStatus


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    listing_id = Column(
        Integer,
        ForeignKey("listings.id")
    )

    start_time = Column(DateTime)
    end_time = Column(DateTime)

    actual_start_time = Column(
        DateTime,
        nullable=True
    )

    actual_end_time = Column(
        DateTime,
        nullable=True
    )

    exit_requested_at = Column(
        DateTime,
        nullable=True
    )

    total_cost = Column(Float)

    status = Column(
        Enum(BookingStatus),
        default=BookingStatus.CONFIRMED
    )

