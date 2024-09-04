from typing import Union, Dict, List
from sqlalchemy.future import select
from decimal import Decimal, ROUND_HALF_UP

from src.backend.config import config
from src.backend.common import custom_exc
from src.backend.schemas import comment_schema
from src.backend.db.models.comment import Comment
from src.backend.db.session import get_db


class CommentDAL:
    def __init__(self, db_session):
        self.session = db_session

    def get_by(self, *, comment_id: int = None) -> Comment:
        if comment_id:
            stmt = select(Comment).where(Comment.CommentId == comment_id)
        else:
            raise custom_exc.EnumException()
        q = self.session.execute(stmt)
        return q.scalar()
    
    def get_by_campaign(self, campaign_id: int) -> List[Comment]:
        stmt = select(Comment).where(Comment.CampaignId == campaign_id)
        q = self.session.execute(stmt)
        return q.scalars().all()

    def get_all_comment(self) -> List[Comment]:
        stmt = select(Comment)
        q = self.session.execute(stmt)
        return q.scalars().all()

    def create_new_comment(self, comment: Union[comment_schema.Comment, Dict]):
        obj = Comment(**comment) if isinstance(comment, dict) else Comment(**comment.dict())
        self.session.add(obj)
        self.session.commit()
        return obj

    def update_comment(self, comment: Union[comment_schema.Comment, Dict]):
        obj = Comment(**comment) if isinstance(comment, dict) else Comment(**comment.dict())
        self.session.merge(obj)
        self.session.commit()
        return obj

    def delete_comment(self, comment_id: int):
        stmt = select(Comment).where(Comment.CommentId == comment_id)
        q = self.session.execute(stmt)
        obj = q.scalar()
        self.session.delete(obj)
        self.session.commit()
        return obj

