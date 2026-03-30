from dataclasses import dataclass

@dataclass
class User:
    id: int | None
    first_name: str
    last_name: str
    address: str | None
    phone_number: str | None
    username: str