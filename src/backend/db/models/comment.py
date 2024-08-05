from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Comment(Base):
    __tablename__ = 'comments'

    CommentId = Column(Integer, primary_key=True, index=True)
    CampaignId = Column(Integer, ForeignKey('campaigns.CampaignId',use_alter=True,name='fk_campaign_id'))
    UserId = Column(Integer, ForeignKey('users.UserId'))
    CommentText = Column(String)
    CreateTime = Column(DateTime)

    campaign = relationship("Campaign", back_populates="comments")
    user = relationship("User", back_populates="comments")