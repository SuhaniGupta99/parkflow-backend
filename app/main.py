from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers.user_router import router as user_router
from app.routers.auth_router import router as auth_router
from app.routers.listing_router import router as listing_router
from app.routers.booking_router import router as booking_router
from app.routers.qr_router import router as qr_router

app = FastAPI(
    title="ParkFlow API",
    version="1.0.0"
)
app.mount(
    "/qr_codes",
    StaticFiles(directory="qr_codes"),
    name="qr_codes"
)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(listing_router)
app.include_router(booking_router)
app.include_router(qr_router)

@app.get("/")
def root():
    return {
        "message": "ParkFlow API Running"
    }