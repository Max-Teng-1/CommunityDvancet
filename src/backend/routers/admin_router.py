from fastapi import APIRouter, Depends

from src.backend.config import config
from src.backend.core import security
from src.backend.common import response
from src.backend.db.depend import DALGetter, get_user
from src.backend.db.models.user import User
from src.backend.db.dals.user_dal import UserDAL
from src.backend.schemas import user_schema
from src.backend.schemas import admin_schema


router = APIRouter()


@router.post("/add", summary="add an admin", description="add an admin")
def add_admin(data: user_schema.Id, user: User = Depends(get_user), dal: UserDAL = Depends(DALGetter(UserDAL))):
    if not user:
        return response.resp_401(message="Your account has expired, Please log in again")
    if user.role != config.SUPER_ADMIN:
        return response.resp_400(message="You are not admin")
    admin = dal.set_admin(data.id)
    return response.resp_200(data=admin.id, message="Admin add success")


@router.post("/remove", summary="remove an admin", description="remove an admin")
def remove_admin(data: user_schema.Id, user: User = Depends(get_user), dal: UserDAL = Depends(DALGetter(UserDAL))):
    if not user:
        return response.resp_401(message="Your account has expired, Please log in again")
    if user.role != config.SUPER_ADMIN:
        return response.resp_400(message="You are not admin")
    dal.delete_user(data.id)
    return response.resp_200(message="Remove success")


@router.get("/list/admin", summary="list all admins", description="list all admins")
def list_admin(user: User = Depends(get_user), dal: UserDAL = Depends(DALGetter(UserDAL))):
    if not user:
        return response.resp_401(message="Your account has expired, Please log in again")
    if user.role < config.ADMIN:
        return response.resp_400(message="You are not admin")
    admins = dal.get_all_admin()
    return response.resp_200(data=admins, message="List admin success")


@router.get("/list/user", summary="list all users", description="list all users")
def list_user(user: User = Depends(get_user), dal: UserDAL = Depends(DALGetter(UserDAL))):
    if not user:
        return response.resp_401(message="Your account has expired, Please log in again")
    if user.role < config.ADMIN:
        return response.resp_400(message="You are not admin")
    users = dal.get_all_user()
    return response.resp_200(data=users, message="List user success")

@router.post("/lock", summary="lock a user", description="lock a user")
def lock_user(data: user_schema.Id, user: User = Depends(get_user), dal: UserDAL = Depends(DALGetter(UserDAL))):
    if not user:
        return response.resp_401(message="Your account has expired, Please log in again")
    if user.role < config.ADMIN:
        return response.resp_400(message="You are not admin")
    dal.lock_user(data.id)
    return response.resp_200(message="Lock success")
