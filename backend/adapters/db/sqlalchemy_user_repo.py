from sqlalchemy.orm import Session
from domain.ports.user_repository import UserRepository
from models import User as DBUser
from domain.entities.user import User as DomainUser

class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_domain(self, db_user: DBUser) -> DomainUser:
        """Convert SQLAlchemy ORM user to domain user."""
        return DomainUser(
            id=db_user.id,
            first_name=db_user.first_name,
            last_name=db_user.last_name,
            address=db_user.address,
            phone_number=db_user.phone_number,
            username=db_user.username
        )

    def save(self, user: DomainUser) -> DomainUser:
        """Create or update a user in the database."""
        db_user = None

        if user.id:
            db_user = self.db.query(DBUser).filter(DBUser.id == user.id).first()
            if db_user:
                # Update only non-None fields
                for key in ["first_name", "last_name", "address", "phone_number", "username"]:
                    value = getattr(user, key, None)
                    if value is not None:
                        setattr(db_user, key, value)

        if not db_user:
            # Create new DB user
            db_user = DBUser(
                first_name=user.first_name,
                last_name=user.last_name,
                address=user.address,
                phone_number=user.phone_number,
                username=user.username
            )
            self.db.add(db_user)

        self.db.commit()
        self.db.refresh(db_user)
        return self._to_domain(db_user)

    def get_by_id(self, user_id: int) -> DomainUser | None:
        db_user = self.db.query(DBUser).filter(DBUser.id == user_id).first()
        return self._to_domain(db_user) if db_user else None

    def list(self, skip: int, limit: int) -> tuple[list[DomainUser], int]:
        db_users = (
            self.db.query(DBUser)
            .order_by(DBUser.id.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        total = self.db.query(DBUser).count()
        domain_users = [self._to_domain(u) for u in db_users]
        return domain_users, total

    def username_exists(self, username: str) -> bool:
        return self.db.query(DBUser).filter(DBUser.username == username).first() is not None