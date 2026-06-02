from datetime import datetime
from pydantic import BaseModel


class BookingCreate(BaseModel):
    listing_id: int

    start_time: datetime

    end_time: datetime


class BookingResponse(BaseModel):
    id: int

    user_id: int

    listing_id: int

    start_time: datetime

    end_time: datetime
    
    actual_start_time: datetime | None = None
    
    actual_end_time: datetime | None = None
    
    exit_requested_at: datetime | None = None

    total_cost: float

    status: str

    class Config:
        from_attributes = True