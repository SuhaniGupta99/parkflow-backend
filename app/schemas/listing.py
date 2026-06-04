from pydantic import BaseModel


class ListingCreate(BaseModel):
    title: str
    address: str

    latitude: float
    longitude: float

    hourly_rate: float

    total_spaces: int

    description: str | None = None


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

    is_active: bool

    class Config:
        from_attributes = True

class NearbyListingResponse(BaseModel):
    id: int

    title: str

    address: str

    latitude: float

    longitude: float

    hourly_rate: float

    available_spaces: int

    distance_km: float
    
class ListingUpdate(BaseModel):
    title: str | None = None

    address: str | None = None

    hourly_rate: float | None = None

    total_spaces: int | None = None

    description: str | None = None

    is_active: bool | None = None