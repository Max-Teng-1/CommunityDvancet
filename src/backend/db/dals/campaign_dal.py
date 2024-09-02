from typing import Union, Dict, List
from sqlalchemy.future import select
from decimal import Decimal, ROUND_HALF_UP

from src.backend.config import config
from src.backend.common import custom_exc
from src.backend.schemas import campaign_schema
from src.backend.db.models.campaign import Campaign
from src.backend.db.session import get_db


class CampaignDAL:
    def __init__(self, db_session):
        self.session = db_session

    def get_by(self, *, campaign_id: int = None, owner_id: int = None, status: int = None) -> Campaign:
        if campaign_id:
            stmt = select(Campaign).where(Campaign.CampaignId == campaign_id)
        elif owner_id:
            stmt = select(Campaign).where(Campaign.OwnerId == owner_id)
        elif status:
            stmt = select(Campaign).where(Campaign.Status == status)
        else:
            raise custom_exc.EnumException()
        q = self.session.execute(stmt)
        return q.scalar()

    def get_all_campaign_by_status(self, status) -> List[Campaign]:
        stmt = select(Campaign).where(Campaign.Status == status)
        q = self.session.execute(stmt)
        return q.scalars().all()

    def get_all_campaign_by_owner(self, owner_id) -> List[Campaign]:
        stmt = select(Campaign).where(Campaign.OwnerId == owner_id)
        q = self.session.execute(stmt)
        return q.scalars().all()

    def create_new_campaign(self, campaign: Union[campaign_schema.Campaign, Dict]):
        obj = Campaign(**campaign) if isinstance(campaign, dict) else Campaign(**campaign.dict())
        self.session.add(obj)
        self.session.commit()
        return obj

    def update_campaign(self, campaign: Union[campaign_schema.Campaign, Dict]):
        obj = Campaign(**campaign) if isinstance(campaign, dict) else Campaign(**campaign.dict())
        self.session.merge(obj)
        self.session.commit()
        return obj

    def delete_campaign(self, campaign_id: int):
        stmt = select(Campaign).where(Campaign.CampaignId == campaign_id)
        q = self.session.execute(stmt)
        obj = q.scalar()
        self.session.delete(obj)

    def like_campaign(self, campaign_id: int):
        stmt = select(Campaign).where(Campaign.CampaignId == campaign_id)
        q = self.session.execute(stmt)
        obj = q.scalar()
        # print(obj)
        # print(obj.Likes)
        obj.Likes += 1
        self.session.merge(obj)
        self.session.commit()
        return obj

    def approve_campaign(self, campaign_id: int):
        stmt = select(Campaign).where(Campaign.CampaignId == campaign_id)
        q = self.session.execute(stmt)
        obj = q.scalar()
        obj.Status = config.APPROVED
        self.session.merge(obj)
        self.session.commit()
        return obj

    def reject_campaign(self, campaign_id: int):
        stmt = select(Campaign).where(Campaign.CampaignId == campaign_id)
        q = self.session.execute(stmt)
        obj = q.scalar()
        obj.Status = config.REJECTED
        self.session.commit()
        self.session.merge(obj)
        return obj

