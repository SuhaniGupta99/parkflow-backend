import json
import os
import qrcode
from geopy.distance import geodesic

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

QR_DIRECTORY = BASE_DIR / "qr_codes"


os.makedirs(QR_DIRECTORY, exist_ok=True)


def generate_listing_qr(
    listing_id: int,
    qr_type: str
):
    os.makedirs(
        QR_DIRECTORY,
        exist_ok=True
    )
    qr_data = {
        "listing_id": listing_id,
        "type": qr_type,
        "version": 1
    }

    filename = (
        f"{qr_type.lower()}_listing_{listing_id}.png"
    )

    filepath = os.path.join(
        QR_DIRECTORY,
        filename
    )

    qr = qrcode.make(
        json.dumps(qr_data)
    )

    qr.save(filepath)

    return filepath

MAX_DISTANCE_METERS = 75

def is_user_near_listing(
    user_lat: float,
    user_lng: float,
    listing_lat: float,
    listing_lng: float
):
    distance = geodesic(
        (user_lat, user_lng),
        (listing_lat, listing_lng)
    ).meters

    return distance <= MAX_DISTANCE_METERS