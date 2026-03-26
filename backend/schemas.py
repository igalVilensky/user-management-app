from pydantic import BaseModel

class UserBase(BaseModel):
    first_name: str
    last_name: str
    address: str | None = None
    phone: str | None = None
    username: str

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True