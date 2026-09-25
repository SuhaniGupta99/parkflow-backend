from pydantic import BaseModel


class ListingCreate(BaseModel):
    title: str
    address: str

    latitude: float
    longitude: float

    hourly_rate: float

    total_spaces: int

    description: str | None = None

    image_url: str | None = None

    amenities: list[str] = []

class ListingResponse(BaseModel):
    id: int

    owner_id: int

    title: str
    address: str

    latitude: float
    longitude: float

    hourly_rate: float

    total_spaces: int
    available_spaces: int

    description: str | None

    image_url: str | None

    amenities: list[str]

    is_active: bool

    owner_name: str

    class Config:
        from_attributes = True

class NearbyListingResponse(BaseModel):
    id: int

    owner_id: int

    title: str

    address: str

    latitude: float

    longitude: float

    hourly_rate: float

    total_spaces: int

    available_spaces: int

    description: str | None = None

    image_url: str | None = None

    amenities: list[str]

    is_active: bool

    distance_km: float

    owner_name: str
    
class ListingUpdate(BaseModel):
    title: str | None = None

    address: str | None = None

    hourly_rate: float | None = None

    total_spaces: int | None = None

    description: str | None = None

    amenities: list[str] | None = None

    is_active: bool | None = None