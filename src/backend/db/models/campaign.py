from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Campaign(Base):
    __tablename__ = 'campaigns'

    CampaignId = Column(Integer, primary_key=True, index=True)
    Name = Column(String)
    Description = Column(String)
    ImageUrl = Column(String)
    Category = Column(Integer)
    Likes = Column(Integer)
    CommentId = Column(Integer, ForeignKey('comments.CommentId'))
    StartTime = Column(DateTime)
    EndTime = Column(DateTime)
    Status = Column(String)
    CreateTime = Column(DateTime)
    UpdateTime = Column(DateTime)
    OwnerId = Column(Integer, ForeignKey('users.UserId',use_alter=True, name='fk_campaignOwner'))

    owner = relationship("User", back_populates="campaigns")
    comments = relationship("Comment", back_populates="campaign")