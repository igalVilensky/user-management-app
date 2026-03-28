import re
from fastapi import APIRouter, Depends, HTTPException, Query
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
@router.post("/", response_model=UserRead, status_code=201)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    user = User(**user_data.model_dump())
    db.add(user)
    
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Database error occurred")
    
    db.refresh(user)
    return user

# Suggest username
@router.get("/suggest-username")
def suggest_username(
    first_name: str = Query(..., min_length=1, max_length=50), 
    last_name: str = Query(..., min_length=1, max_length=50),
    db: Session = Depends(get_db)
):
    base = f"{first_name}.{last_name}".lower()
    # Remove any invalid characters for username
    base = re.sub(r'[^a-z0-9.]', '', base)
    username = base
    counter = 1

    while db.query(User).filter(User.username == username).first():
        username = f"{base}{counter}"
        counter += 1

    return {"username": username}

# READ all users
@router.get("/", response_model=UserList)
def get_users(
    skip: int = Query(0, ge=0), 
    limit: int = Query(10, ge=1, le=100), 
    db: Session = Depends(get_db)
):
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

    # If username is being updated, check it doesn't conflict
    if user_data.username and user_data.username != user.username:
        existing_user = db.query(User).filter(User.username == user_data.username).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")

    update_data = user_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Database error occurred")

    db.refresh(user)
    return user

# DELETE user by ID
@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return None