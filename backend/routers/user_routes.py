from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import get_db
from models import User
from schemas import UserCreate, UserRead, UserUpdate, UserList

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# CREATE user
@router.post("/", response_model=UserRead)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    user = User(**user_data.model_dump(exclude_unset=True))
    db.add(user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username already exists")

    db.refresh(user)
    return user

# Suggest username
@router.get("/suggest-username")
def suggest_username(first_name: str, last_name: str, db: Session = Depends(get_db)):
    base = f"{first_name}.{last_name}".lower()
    username = base
    counter = 1

    while db.query(User).filter(User.username == username).first():
        username = f"{base}{counter}"
        counter += 1

    return {"username": username}

# READ all users
@router.get("/", response_model=UserList)
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.id.desc()).offset(skip).limit(limit).all()
    total_count = db.query(User).count()
    return {"users": users, "total_count": total_count}

# READ single user by ID
@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# UPDATE user by ID
@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user_data.model_dump(exclude_unset=True).items():
        setattr(user, key, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username already exists")

    db.refresh(user)
    return user

# DELETE user by ID
@router.delete("/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted"}