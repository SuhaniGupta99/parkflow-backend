from enum import Enum


class UserRole(str, Enum):
    HOST = "HOST"
    CUSTOMER = "CUSTOMER"

class BookingStatus(str, Enum):
    CONFIRMED = "CONFIRMED"
    ACTIVE = "ACTIVE"
    EXIT_REQUESTED = "EXIT_REQUESTED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"