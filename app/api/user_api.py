from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin
from app.models.user import User
from app.auth.auth import hash_password, verify_password
from app.auth.jwt_utils import create_access_token
from datetime import datetime
from app.database import get_db

router = APIRouter()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    new_user = User(
        username=user.username,
        displayname=user.displayname,
        hashedpasswd=hash_password(user.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User registered successfully"}

@router.post("/login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == credentials.username).first()
    if not user or not verify_password(credentials.password, user.hashedpasswd):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    user.last_login = datetime.utcnow()
    db.commit()
    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer", "displayname": user.displayname}
