from sqlalchemy import Column, Integer, String, Boolean, func, or_

from app.utils.hash import make_hash, hash_verify
from app.db import Base, SessionLocal


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False, unique=True)
    email = Column(String(128), nullable=False, unique=True)
    password_hash = Column(String(128), nullable=False)
    online = Column(Boolean, default=False)
    logged_in = Column(Boolean, default=False)
    connection_id = Column(String(64), nullable=True)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, value: str):
        self.password_hash = make_hash(value)

    @classmethod
    def authenticate(cls, db: SessionLocal, user_id: str, password: str):
        user = (
            db.query(cls)
            .filter(
                or_(
                    func.lower(cls.username) == func.lower(user_id),
                    func.lower(cls.email) == func.lower(user_id),
                )
            )
            .first()
        )
        if user is not None and hash_verify(password, user.password):
            return user

    def __repr__(self):
        return f"<{self.id}: [{self.username}]-[{self.email}]>"
