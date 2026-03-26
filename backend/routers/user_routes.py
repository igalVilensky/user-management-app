from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserCreate, UserRead

router = APIRouter()

# CREATE user
@router.post("/users/", response_model=UserRead)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user_data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    user = User(**user_data.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# READ all users
@router.get("/users/", response_model=list[UserRead])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# READ single user by ID
@router.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# UPDATE user by ID
@router.put("/users/{user_id}", response_model=UserRead)
def update_user(user_id: int, user_data: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user_data.dict().items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

# DELETE user by ID
@router.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted"}