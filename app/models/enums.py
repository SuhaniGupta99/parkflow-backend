from enum import Enum


class UserRole(str, Enum):
    HOST = "HOST"
    CUSTOMER = "CUSTOMER"