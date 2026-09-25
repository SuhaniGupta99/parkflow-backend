from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    Enum
)
from sqlalchemy.orm import relationship

from app.database import Base

import enum


class VehicleType(str, enum.Enum):
    CAR = "CAR"
    BIKE = "BIKE"


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    vehicle_type = Column(
        Enum(VehicleType),
        nullable=False,
    )

    make_model = Column(
        String,
        nullable=False,
    )

    license_plate = Column(
        String,
        nullable=False,
    )

    is_electric = Column(
        Boolean,
        default=False,
    )

    color = Column(
        String,
        nullable=False,
    )

    is_default = Column(
        Boolean,
        default=False,
    )

    user = relationship(
        "User",
        back_populates="vehicles",
    )