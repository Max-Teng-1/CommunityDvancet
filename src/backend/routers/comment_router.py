import random
from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, File, UploadFile, Response

from src.backend.config import config
from src.backend.core import security
from src.backend.common import response
from src.backend.db.depend import DALGetter, get_user
from src.backend.db.models.user import User
from src.backend.db.dals.user_dal import UserDAL
from src.backend.db.models.campaign import Campaign
from src.backend.db.dals.campaign_dal import CampaignDAL
from src.backend.schemas import comment_schema
from src.backend.db.models.comment import Comment
from src.backend.db.dals.comment_dal import CommentDAL

router = APIRouter()


@router.post("/create", summary="create a comment", description="create a comment")
def create_comment(data: comment_schema.Comment, user: User = Depends(get_user), dal: CommentDAL = Depends(DALGetter(CommentDAL))):
    if not user:
        return response.resp_401(message="Your account has expired, Please log in again")
    comment = dal.create_new_comment(dict(
        CampaignId=data.campaign_id,
        UserId=user.UserId,
        CommentText=data.comment_text,
        CreateTime=datetime.utcnow()
    ))
    return response.resp_200(data=comment, message="Comment create success")

@router.get("/get", summary="get a comment", description="get a comment")
def get_comment(data: comment_schema.Get, dal: CommentDAL = Depends(DALGetter(CommentDAL))):
    comment = dal.get_by(comment_id=data.comment_id)
    return response.resp_200(data=comment, message="Comment get success")

@router.get("/get_by_campaign", summary="get all comments by campaign", description="get all comments by campaign")
def get_comment_by_campaign(data: comment_schema.GetByCampaign, dal_comment: CommentDAL = Depends(DALGetter(CommentDAL)), dal_user: UserDAL = Depends(DALGetter(UserDAL))):
    comments = dal_comment.get_by_campaign(campaign_id=data.campaign_id)
    dict_comments = []
    for comment in comments:
        dict_comment = comment.__dict__
        dict_comment["Avatar"] = dal_user.get_by(user_id=comment.UserId).Avatar
        dict_comment["Username"] = dal_user.get_by(user_id=comment.UserId).Username
        dict_comments.append(dict_comment)
    sorted_comments = sorted(dict_comments, key=lambda x: x["CreateTime"], reverse=True)
    return response.resp_200(data=sorted_comments, message="Comment get by campaign success")

@router.get("/get_all", summary="get all comments", description="get all comments")
def get_all_comment(dal: CommentDAL = Depends(DALGetter(CommentDAL))):
    comments = dal.get_all_comment()
    return response.resp_200(data=comments, message="Comment get all success")

# @router.put("/update", summary="update a comment", description="update a comment")
# def update_comment(data: comment_schema.Update, user: User = Depends(get_user), dal: CommentDAL = Depends(DALGetter(CommentDAL))):
#     if not user:
#         return response.resp_401(message="Your account has expired, Please log in again")
#     comment = dal.update_comment(dict(
#         CommentId=data.comment_id,
#         Content=data.content
#     ))
#     return response.resp_200(data=comment.CommentId, message="Comment update success")

# @router.delete("/delete", summary="delete a comment", description="delete a comment")
# def delete_comment(data: comment_schema.Delete, user: User = Depends(get_user), dal: CommentDAL = Depends(DALGetter(CommentDAL))):
#     if not user:
#         return response.resp_401(message="Your account has expired, Please log in again")
#     dal.delete_comment(comment_id=data.comment_id)
#     return response.resp_200(message="Comment delete success")

