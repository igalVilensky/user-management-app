from pydantic import BaseModel, Field

class UserBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    address: str | None = None
    phone_number: str | None = None
    username: str = Field(..., min_length=3)

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    first_name: str | None = Field(None, min_length=1, max_length=50)
    last_name: str | None = Field(None, min_length=1, max_length=50)
    address: str | None = None
    phone_number: str | None = None
    username: str | None = Field(None, min_length=3)

class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True