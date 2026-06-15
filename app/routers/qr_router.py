from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database import get_db

from app.core.dependencies import (
    get_current_user
)

from app.repositories.listing_repository import (
    get_listing_by_id
)

from app.repositories.booking_repository import (
    get_booking_by_id,
    check_in_booking,
    request_exit_booking
)

from app.schemas.qr import (
    QRResponse,
    QRScanRequest
)

from app.services.qr_service import (
    generate_listing_qr,
    is_user_near_listing
)

router = APIRouter(
    prefix="/qr",
    tags=["QR"]
)


@router.post(
    "/generate/{listing_id}",
    response_model=QRResponse
)
def generate_qr(
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

    entry_qr = generate_listing_qr(
        listing_id,
        "ENTRY"
    )

    exit_qr = generate_listing_qr(
        listing_id,
        "EXIT"
    )

    return {
    "listing_id": listing_id,
    "entry_qr_path":
        f"/qr_codes/entry_listing_{listing_id}.png",

    "exit_qr_path":
        f"/qr_codes/exit_listing_{listing_id}.png"
    }


@router.post("/scan")
def scan_qr(
    request: QRScanRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    booking = get_booking_by_id(
        db,
        request.booking_id
    )

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    # Booking ownership check
    if booking.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not your booking"
        )

    # QR listing must match booking listing
    if booking.listing_id != request.listing_id:
        raise HTTPException(
            status_code=400,
            detail="Listing mismatch"
        )

    listing = get_listing_by_id(
        db,
        request.listing_id
    )

    if not listing:
        raise HTTPException(
            status_code=404,
            detail="Listing not found"
        )

    # Geofence validation
    is_near = is_user_near_listing(
        request.latitude,
        request.longitude,
        listing.latitude,
        listing.longitude
    )

    if not is_near:
        raise HTTPException(
            status_code=403,
            detail="Too far from parking location"
        )

    # ENTRY QR
    if request.qr_type == "ENTRY":

        if booking.status != "CONFIRMED":
            raise HTTPException(
                status_code=400,
                detail="Booking must be CONFIRMED"
            )

        return check_in_booking(
            db,
            booking
        )

    # EXIT QR
    if request.qr_type == "EXIT":

        if booking.status != "ACTIVE":
            raise HTTPException(
                status_code=400,
                detail="Booking must be ACTIVE"
            )

        return request_exit_booking(
            db,
            booking
        )

    raise HTTPException(
        status_code=400,
        detail="Invalid QR type"
    )