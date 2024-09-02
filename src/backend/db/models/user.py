# backend/db/models/user.py
import re
from passlib.context import CryptContext
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

from src.backend.config import config


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class User(Base):
    __tablename__ = 'users'

    UserId = Column(Integer, primary_key=True, index=True)
    Username = Column(String)
    Password = Column(String)
    RoleId = Column(Integer, ForeignKey('roles.RoleId', use_alter= True, name='fk_user_role'))
    Gender = Column(Integer)
    Birthday = Column(DateTime)
    Avatar = Column(String)
    Email = Column(String, unique=True, index=True)
    CreateTime = Column(DateTime)
    UpdateTime = Column(DateTime)

    role = relationship("Role", back_populates="users")
    password_recoveries = relationship("PasswordRecovery", back_populates="user")
    comments = relationship("Comment", back_populates="user", foreign_keys="[Comment.UserId]")
    campaigns = relationship("Campaign", back_populates="owner", foreign_keys="[Campaign.OwnerId]")

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        verify password
        :param plain_password: entered password
        :param hashed_password: hashed stored password
        :return:

        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        get hashed password
        :param password:
        :return:
        """
        return pwd_context.hash(password)

    @staticmethod
    def verify_email_regex(email: str):
        """
        :param email
        :return:
        """
        return re.fullmatch(config.EMAIL_REGEX, email)

    @staticmethod
    def verify_confirm_password(password_1: str, password_2: str):
        return password_1 == password_2