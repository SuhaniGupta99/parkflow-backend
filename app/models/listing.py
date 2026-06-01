from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    ForeignKey
)

from app.database import Base


class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)

    owner_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    title = Column(
        String,
        nullable=False
    )

    address = Column(
        String,
        nullable=False
    )

    latitude = Column(
        Float,
        nullable=False
    )

    longitude = Column(
        Float,
        nullable=False
    )

    hourly_rate = Column(
        Float,
        nullable=False
    )

    total_spaces = Column(
        Integer,
        nullable=False
    )

    available_spaces = Column(
        Integer,
        nullable=False
    )

    description = Column(
        String,
        nullable=True
    )

    is_active = Column(
        Boolean,
        default=True
    )