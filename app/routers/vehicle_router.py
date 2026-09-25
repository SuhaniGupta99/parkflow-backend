from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from app.models.user import User
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.booking import Booking
from app.models.enums import BookingStatus
from app.core.dependencies import (
    get_current_user,
)

from app.models.vehicle import Vehicle

from app.schemas.vehicle import (
    VehicleCreate,
    VehicleResponse,
    VehicleUpdate,
)

from app.repositories.vehicle_repository import (
    create_vehicle,
    get_my_vehicles,
    get_vehicle_by_id,
    update_vehicle,
    delete_vehicle,
)

router = APIRouter(
    prefix="/vehicles",
    tags=["Vehicles"],
)


@router.post(
    "/",
    response_model=VehicleResponse,
)
def create_new_vehicle(
    vehicle: VehicleCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    new_vehicle = Vehicle(
        user_id=current_user.id,
        vehicle_type=vehicle.vehicle_type,
        make_model=vehicle.make_model,
        license_plate=vehicle.license_plate,
        is_electric=vehicle.is_electric,
        color=vehicle.color,
        is_default=vehicle.is_default,
    )

    return create_vehicle(
        db,
        new_vehicle,
    )


@router.get(
    "/my",
    response_model=list[VehicleResponse],
)
def get_current_user_vehicles(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_my_vehicles(
        db,
        current_user.id,
    )


@router.put(
    "/{vehicle_id}",
    response_model=VehicleResponse,
)
def modify_vehicle(
    vehicle_id: int,
    vehicle_data: VehicleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    vehicle = (
        db.query(Vehicle)
        .filter(
            Vehicle.id == vehicle_id,
            Vehicle.user_id == current_user.id,
        )
        .first()
    )

    if not vehicle:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found",
        )

    if vehicle_data.is_default:

        db.query(Vehicle).filter(
            Vehicle.user_id == current_user.id
        ).update(
            {
                Vehicle.is_default: False
            }
        )

    return update_vehicle(
        db=db,
        vehicle=vehicle,
        vehicle_type=vehicle_data.vehicle_type,
        make_model=vehicle_data.make_model,
        license_plate=vehicle_data.license_plate,
        is_electric=vehicle_data.is_electric,
        color=vehicle_data.color,
        is_default=vehicle_data.is_default,
    )

@router.delete(
    "/{vehicle_id}",
)
def remove_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    vehicle = get_vehicle_by_id(
        db,
        vehicle_id,
    )

    if not vehicle:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found",
        )

    if vehicle.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized",
        )
    active_booking = (
        db.query(Booking)
        .filter(
            Booking.vehicle_id == vehicle.id,
            Booking.status.in_(
                [
                    BookingStatus.PENDING,
                    BookingStatus.CONFIRMED,
                    BookingStatus.ACTIVE,
                    BookingStatus.EXIT_REQUESTED,
                ]
            ),
       
    )
    .first()
    )
    if active_booking:
        raise HTTPException(
            status_code=400,
            detail="Vehicle has active bookings and cannot be deleted.",
        )
    if vehicle.is_default:
        replacement = (
            db.query(Vehicle)
            .filter(
                Vehicle.user_id == current_user.id,
                Vehicle.id != vehicle.id,
            )
            .order_by(Vehicle.id)
            .first()
        )
        if replacement:
            replacement.is_default = True
  
    delete_vehicle(
        db,
        vehicle,
    )

    return {
        "message": "Vehicle deleted successfully",
    }