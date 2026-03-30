from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from infrastructure.database import get_db
from domain.services.user_service import UserService
from adapters.db.sqlalchemy_user_repo import SQLAlchemyUserRepository
from schemas import UserCreate, UserRead, UserUpdate, UserList
from domain.entities.user import User as DomainUser

router = APIRouter(prefix="/users", tags=["users"])

def get_service(db: Session = Depends(get_db)):
    repo = SQLAlchemyUserRepository(db)
    return UserService(repo)

# CREATE
@router.post("/", response_model=UserRead, status_code=201)
def create_user(user_data: UserCreate, service: UserService = Depends(get_service)):
    domain_user = DomainUser(id=None, **user_data.model_dump())
    try:
        saved_user = service.create_user(domain_user)
        return saved_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# SUGGEST USERNAME
@router.get("/suggest-username")
def suggest_username(
    first_name: str = Query(..., min_length=1, max_length=50),
    last_name: str = Query(..., min_length=1, max_length=50),
    service: UserService = Depends(get_service)
):
    return {"username": service.suggest_username(first_name, last_name)}

# LIST
@router.get("/", response_model=UserList)
def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    service: UserService = Depends(get_service)
):
    users, total_count = service.list_users(skip, limit)
    return {"users": users, "total_count": total_count}

# READ single
@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, service: UserService = Depends(get_service)):
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# UPDATE
@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: int, user_data: UserUpdate, service: UserService = Depends(get_service)):
    existing_user = service.get_user(user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    # merge updates
    for k, v in user_data.model_dump(exclude_unset=True).items():
        setattr(existing_user, k, v)
    try:
        return service.create_user(existing_user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# DELETE
@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, service: UserService = Depends(get_service)):
    deleted = service.repo.delete(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return None