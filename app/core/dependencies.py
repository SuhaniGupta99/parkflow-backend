from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.auth import verify_access_token
from app.repositories.user_repository import get_user_by_id

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    payload = verify_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user = get_user_by_id(
        db,
        payload["user_id"]
    )

    print("USER:", user)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user