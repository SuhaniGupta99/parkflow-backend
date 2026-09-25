from pydantic import BaseModel
from app.models.vehicle import VehicleType


class VehicleCreate(BaseModel):
    vehicle_type: VehicleType

    make_model: str

    license_plate: str

    is_electric: bool

    color: str

    is_default: bool = False


class VehicleResponse(BaseModel):
    id: int

    user_id: int

    vehicle_type: VehicleType

    make_model: str

    license_plate: str

    is_electric: bool

    color: str

    is_default: bool

    class Config:
        from_attributes = True


class VehicleUpdate(BaseModel):
    vehicle_type: VehicleType | None = None

    make_model: str | None = None

    license_plate: str | None = None

    is_electric: bool | None = None

    color: str | None = None

    is_default: bool | None = None