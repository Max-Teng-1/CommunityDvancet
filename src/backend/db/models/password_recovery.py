from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class PasswordRecovery(Base):
    __tablename__ = 'password_recoveries'

    RecoveryId = Column(Integer, primary_key=True, index=True)
    UserId = Column(Integer, ForeignKey('users.UserId'))
    Token = Column(String)
    CreatedAt = Column(DateTime)
    ExpireAt = Column(DateTime)

    user = relationship("User", back_populates="password_recoveries")