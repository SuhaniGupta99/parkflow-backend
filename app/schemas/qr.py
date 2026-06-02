from pydantic import BaseModel


class QRResponse(BaseModel):
    listing_id: int

    entry_qr_path: str

    exit_qr_path: str


class QRScanRequest(BaseModel):
    booking_id: int

    listing_id: int

    qr_type: str

    latitude: float

    longitude: float