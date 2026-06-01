from fastapi import FastAPI

from app.routers.user_router import router as user_router
from app.routers.auth_router import router as auth_router
app = FastAPI(
    title="ParkFlow API",
    version="1.0.0"
)

app.include_router(user_router)
app.include_router(auth_router)


@app.get("/")
def root():
    return {
        "message": "ParkFlow API Running"
    }