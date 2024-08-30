import random
from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, File, UploadFile, Response

from src.backend.config import config
from src.backend.core import security
from src.backend.common import response
from src.backend.db.depend import DALGetter, get_user
from src.backend.db.models.campaign import Campaign
from src.backend.db.models.user import User
from src.backend.db.dals.user_dal import UserDAL
from src.backend.db.dals.campaign_dal import CampaignDAL
from src.backend.schemas import campaign_schema

router = APIRouter()

@router.post("/create", summary="create a campaign", description="create a campaign")
def create_campaign(data: campaign_schema.Campaign, user: User = Depends(get_user), dal: CampaignDAL = Depends(DALGetter(CampaignDAL))):
    if not user:
        return response.resp_401(message="Your account has expired, Please log in again")
    campaign = dal.create_new_campaign(dict(
        Title=data.title,
        Description=data.description,
        ImageUrl=data.image,
        OwnerId=user.UserId,
        Status=config.PENDING,
        CreateTime=datetime.utcnow(),
        UpdateTime=datetime.utcnow(),
        Likes=0,
    ))
    return response.resp_200(data=campaign.CampaignId, message="Campaign create success")

@router.get("/get", summary="get a campaign", description="get a campaign")
def get_campaign(data: campaign_schema.Get, dal: CampaignDAL = Depends(DALGetter(CampaignDAL))):
    campaign = dal.get_by(campaign_id=data.campaign_id)
    return response.resp_200(data=campaign, message="Campaign get success")

@router.get("/get_all", summary="get all campaigns", description="get all campaigns")
def get_all_campaign(dal: CampaignDAL = Depends(DALGetter(CampaignDAL))):
    campaigns = dal.get_all_campaign()
    return response.resp_200(data=campaigns, message="Campaign get all success")

@router.put("/update", summary="update a campaign", description="update a campaign")
def update_campaign(data: campaign_schema.Update, user: User = Depends(get_user), dal: CampaignDAL = Depends(DALGetter(CampaignDAL))):
    if not user:
        return response.resp_401(message="Your account has expired, Please log in again")
    campaign = dal.update_campaign(dict(
        CampaignId=data.campaign_id,
        Title=data.title,
        Description=data.description,
        ImageUrl=data.image
    ))
    return response.resp_200(data=campaign.CampaignId, message="Campaign update success")

@router.delete("/delete", summary="delete a campaign", description="delete a campaign")
def delete_campaign(data: campaign_schema.Delete, user: User = Depends(get_user), dal: CampaignDAL = Depends(DALGetter(CampaignDAL))):
    if not user:
        return response.resp_401(message="Your account has expired, Please log in again")
    dal.delete_campaign(campaign_id=data.campaign_id)
    return response.resp_200(message="Campaign delete success")

@router.put("/like", summary="like a campaign", description="like a campaign")
def like_campaign(data: campaign_schema.Like, user: User = Depends(get_user), dal: CampaignDAL = Depends(DALGetter(CampaignDAL))):
    if not user:
        return response.resp_401(message="Your account has expired, Please log in again")
    dal.like_campaign(campaign_id=data.campaign_id)
    return response.resp_200(message="Campaign like success")

