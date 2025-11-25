from fastapi import APIRouter, FastAPI, Depends, HTTPException, status
from schemas.schemas import LoginRequest, LoginResponse
from routes.register import verify_password
from sqlalchemy.orm import Session
from core.security import create_access_token
from core.database import get_db
from models.users import User


router = APIRouter(tags=["Login"])

@router.post("/login")
def login(credentials: LoginRequest,
          db: Session = Depends(get_db)):

    user = db.query(User).filter(User.username ==credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    # Create JWT token
    access_token = create_access_token({"sub": user.username})

    return LoginResponse(
        access_token=access_token,
        token_type="bearer"
    )
