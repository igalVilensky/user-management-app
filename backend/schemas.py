from pydantic import BaseModel, Field, field_validator
import re

class UserBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    address: str | None = None
    phone_number: str | None = None
    username: str = Field(..., min_length=3, max_length=50)

    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, v):
        if v is None or v == "":
            return v
        # Allow numbers, spaces, dashes, parentheses, plus sign
        if not re.match(r"^[\+\d\s\-\(\)]{8,20}$", v):
            raise ValueError("Phone number must be 8-20 characters (numbers, spaces, dashes, parentheses, +)")
        return v

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_name(cls, v):
        if v and not re.match(r"^[a-zA-Z\s\-']{1,50}$", v):
            raise ValueError("Name must contain only letters, spaces, hyphens, or apostrophes")
        return v

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    first_name: str | None = Field(None, min_length=1, max_length=50)
    last_name: str | None = Field(None, min_length=1, max_length=50)
    address: str | None = None
    phone_number: str | None = None
    username: str | None = Field(None, min_length=3, max_length=50)

    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, v):
        if v is None or v == "":
            return v
        if not re.match(r"^[\+\d\s\-\(\)]{8,20}$", v):
            raise ValueError("Phone number must be 8-20 characters (numbers, spaces, dashes, parentheses, +)")
        return v

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_name(cls, v):
        if v and not re.match(r"^[a-zA-Z\s\-']{1,50}$", v):
            raise ValueError("Name must contain only letters, spaces, hyphens, or apostrophes")
        return v

class UserRead(UserBase):
    id: int

    model_config = {
        "from_attributes": True
    }

class UserList(BaseModel):
    users: list[UserRead]
    total_count: int