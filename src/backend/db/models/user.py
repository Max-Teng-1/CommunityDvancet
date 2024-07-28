# backend/db/models/user.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class User(Base):
    __tablename__ = 'users'

    UserId = Column(Integer, primary_key=True, index=True)
    Username = Column(String)
    Password = Column(String)
    RoleId = Column(Integer, ForeignKey('roles.RoleId'))
    Gender = Column(Integer)
    Birthday = Column(DateTime)
    Email = Column(String, unique=True, index=True)
    CreateTime = Column(DateTime)
    UpdateTime = Column(DateTime)

    role = relationship("Role", back_populates="users")
    password_recoveries = relationship("PasswordRecovery", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    campaigns = relationship("Campaign", back_populates="owner")