from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class Role(Base):
    __tablename__ = 'roles'

    RoleId = Column(Integer, primary_key=True, index=True)
    RoleName = Column(String, unique=True)
    Description = Column(String)

    users = relationship("User", back_populates="role")