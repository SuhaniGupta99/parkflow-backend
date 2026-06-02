from app.database import Base, engine

from app.models.user import User
from app.models.listing import Listing
from app.models.booking import Booking

Base.metadata.create_all(bind=engine)

print("Tables created successfully!")