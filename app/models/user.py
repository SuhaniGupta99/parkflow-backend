# app/models/user.py

from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy import Enum
from app.models.enums import UserRole


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String, nullable=False)

    email = Column(String, unique=True, nullable=False)

    phone_number = Column(String, nullable=False)
    
    role = Column(Enum(UserRole),nullable=False)

    password_hash = Column(String, nullable=False)