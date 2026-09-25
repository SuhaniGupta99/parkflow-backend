from sqlalchemy.orm import Session

from app.models.vehicle import Vehicle


def create_vehicle(
    db: Session,
    vehicle: Vehicle,
):
    # If this vehicle is marked as default,
    # remove default from all other vehicles
    if vehicle.is_default:

        (
            db.query(Vehicle)
            .filter(
                Vehicle.user_id == vehicle.user_id
            )
            .update(
                {
                    Vehicle.is_default: False
                }
            )
        )

    # If this is the user's first vehicle,
    # make it default automatically.
    existing = (
        db.query(Vehicle)
        .filter(
            Vehicle.user_id == vehicle.user_id
        )
        .count()
    )

    if existing == 0:
        vehicle.is_default = True

    db.add(vehicle)

    db.commit()

    db.refresh(vehicle)

    return vehicle


def get_my_vehicles(
    db: Session,
    user_id: int,
):
    return (
        db.query(Vehicle)
        .filter(
            Vehicle.user_id == user_id
        )
        .order_by(Vehicle.id)
        .all()
    )


def get_vehicle_by_id(
    db: Session,
    vehicle_id: int,
):
    return (
        db.query(Vehicle)
        .filter(
            Vehicle.id == vehicle_id
        )
        .first()
    )




def update_vehicle(
    db: Session,
    vehicle: Vehicle,
    vehicle_type: str,
    make_model: str,
    license_plate: str,
    is_electric: bool,
    color: str,
    is_default: bool,
):
    vehicle.vehicle_type = vehicle_type
    vehicle.make_model = make_model
    vehicle.license_plate = license_plate
    vehicle.is_electric = is_electric
    vehicle.color = color
    vehicle.is_default = is_default

    db.commit()
    db.refresh(vehicle)

    return vehicle


def delete_vehicle(
    db: Session,
    vehicle: Vehicle,
):
    db.delete(vehicle)

    db.commit()