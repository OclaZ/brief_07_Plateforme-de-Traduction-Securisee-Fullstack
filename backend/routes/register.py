from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db, engine
from models.users import User, Base
from passlib.context import CryptContext
from schemas.schemas import UserCreate, UserOut

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


router = APIRouter(tags=["Register"])


@router.post("/register", response_model=UserOut)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):

    # Check username
    
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    safe_password = user.password[:72]

    hashed_password = pwd_context.hash(safe_password)

    new_user = User(
        username=user.username,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/users/{user_id}")
def get_user_debug(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "username": user.username,
        "hashed_password": user.hashed_password
    }
