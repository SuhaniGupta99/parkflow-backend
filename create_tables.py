# create_tables.py

from app.database import engine, Base

# Import models so SQLAlchemy knows about them
from app.models.user import User

Base.metadata.create_all(bind=engine)

print("Tables created successfully!")