from pydantic import BaseModel, EmailStr
from app.models.enums import UserRole


class RegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: str
    role: UserRole
    password: str