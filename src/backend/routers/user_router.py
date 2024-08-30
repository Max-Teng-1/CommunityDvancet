import random
from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, File, UploadFile, Response

from src.backend.config import config
from src.backend.core import security
from src.backend.common import response
from src.backend.db.depend import DALGetter, get_user
from src.backend.db.models.user import User
from src.backend.db.dals.user_dal import UserDAL
from src.backend.schemas import user_schema
from src.backend.routers.helper import send_email, get_aus_time_str
# from src.backend.routers.helper import *

router = APIRouter()

# @router.get("/token/authantication", summary="authantication", description="authantication")
# def token_authantication(user: User = Depends(get_user)):
#     if not user:
#         return response.resp_401(message="Your account has expired, Please log in again")
#     return response.resp_200(data=user, message="Authantication success")

# @router.post("/security_key/verify", summary="check whether security key expired", description="check whether security key expired")
# def security_verify(data: user_schema.SecurityKey, user: User = Depends(get_user)):
#     if not security.check_security_key(data.security_key):
#         if data.password == "":
#             return response.resp_403(message="You need to enter your password for following operations")
#         if data.password != "" and not User.verify_password(data.password, user.password):
#             return response.resp_403(message="Wrong password")
#     security_key = security.create_security_key(expires_delta=timedelta(minutes=config.SECURITY_KEY_EXPIRE_MINUTES))
#     return response.resp_200(data=dict(security_key=security_key), message="Security key verify")

@router.post("/password/verify", summary="verify pwd", description="verify pwd")
def pwd_verify(data: user_schema.PwdVerify, user: User = Depends(get_user)):
    # error check
    if not User.verify_password(data.password, user.password):
        return response.resp_400(message="Wrong password")
    return response.resp_200(message="Password verify success")


@router.post("/register", summary="register for user", description="register for user")
def user_register(data: user_schema.Register, dal: UserDAL = Depends(DALGetter(UserDAL))):
    # error check
    if not User.verify_email_regex(data.email):
        return response.resp_400(message="Invalid Email")
    if dal.get_by(email=data.email):
        return response.resp_400(message="Email has been used")
    if not User.verify_confirm_password(data.password_1, data.password_2):
        return response.resp_400(message="Different passwords")

    # create new user
    new_user = dal.create_new_user(dict(
        Email=data.email,
        Username=data.username,
        Password=User.get_password_hash(data.password_1),
        RoleId=data.role,
        CreateTime=datetime.utcnow(),  # Add creation time
        UpdateTime=datetime.utcnow()   # Add update time
    ))
    return response.resp_200(data=new_user.UserId, message="User Register success")



@router.post("/login", summary="login", description="login")
def user_login(data: user_schema.Login, dal: UserDAL = Depends(DALGetter(UserDAL))):
    user = dal.get_by(email=data.email)
    # error check
    if not user:
        return response.resp_400(message="User not exist (email not registered)")
    if not User.verify_password(data.password, user.Password):
        return response.resp_400(message="Wrong password")
    # create token and login
    token = security.create_access_token(user_id=user.UserId, user_role=user.role, expires_delta=timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES))
    # security_key = security.create_security_key(expires_delta=timedelta(minutes=config.SECURITY_KEY_EXPIRE_MINUTES))

    # dal.update_profile({"recent_log": get_aus_time_str() + "+"}, user.id)
    # return response.resp_200(data=dict(token=token, user=user, security_key=security_key), message="Login success")
    return response.resp_200(data=dict(token=token, user=user), message="Login success")


@router.get("/logout", summary="logout", description="logout", dependencies=[Depends(get_user)])
def logout(user: User = Depends(get_user)):
    # error check
    if not user:
        return response.resp_401(message="Your account has expired, Please log in again")
    return response.resp_200(message="Logout success")


@router.get("/profile", summary="profile of user", description="profile of user")
def profile(user: User = Depends(get_user)):
    # error check
    if not user:
        return response.resp_401(message="Your account has expired, Please log in again")
    return response.resp_200(data=user, message="Get profile success")


@router.post("/profile/update", summary="update profile of user",  description="update profile of user")
def profile_update(data: user_schema.Update, user: User = Depends(get_user), dal: UserDAL = Depends(DALGetter(UserDAL))):
    # error check
    if not user:
        return response.resp_401(message="Your account has expired, Please log in again")

    if not User.verify_email_regex(data.email):
        return response.resp_400(message="Invalid Email")
    if dal.get_by(email=data.email) and dal.get_by(email=data.email).id != user.id:
        return response.resp_400(message="Email has been used")
    # if not User.verify_phone(data.phone):
    #     return response.resp_400(message="Invalid Phone Number")
    # if not User.verify_first_last_name(data.first_name, data.last_name):
    #     return response.resp_400(message="Invalid Name")
    return response.resp_200(data=dal.update_profile(data, user.id), message='Update profile success')


# @router.post("/profile/avatar/update", summary="update avatar of user", description="update avatar of user")
# async def create_upload_file(user: User = Depends(get_user), dal: UserDAL = Depends(DALGetter(UserDAL)), file: UploadFile = File(...)):
#     # error check
#     if not user:
#         return response.resp_401(message="Your account has expired, Please log in again")
#     try:
#         with open(config.USER_AVATAR_PATH + f"{user.id}.png", "wb") as buffer:
#             buffer.write(await file.read())
#     except Exception:
#         return response.resp_400(message="Upload avatar failed")
#     return response.resp_200(data=dal.update_avatar(config.USER_AVATAR_PATH + f"{user.id}.png", user.id), message="Update avatar success")


@router.post("/profile/password/reset", summary="reset pwd", description="reset pwd")
def pwd_reset_reset(data: user_schema.PwdReset, user: User = Depends(get_user), dal: UserDAL = Depends(DALGetter(UserDAL))):
    # error check
    if not user:
        return response.resp_401(message="Your account has expired, Please log in again")

    if not User.verify_password(data.password_old, user.password):
        return response.resp_400(message="Wrong password")
    # if not User.password_check(data.password_1):
    #     return response.resp_400(message="Password invalid")
    if not User.verify_confirm_password(data.password_1, data.password_2):
        return response.resp_400(message="Different passwords")
    # update password
    return response.resp_200(data=dal.update_password(data.password_1, user.id), message="Change Password Success")


@router.post("/password/forgot/request", summary="request change pwd", description="request change pwd")
def pwd_reset_request(data: user_schema.PwdResetRequest, dal: UserDAL = Depends(DALGetter(UserDAL))):
    # error check
    if not User.verify_email_regex(data.email):
        return response.resp_400(message="Invalid Email")
    if not dal.get_by(email=data.email):
        return response.resp_400(message="User not exist (email not registered)")

    # send email
    reset_code = str(random.randint(100000, 999999))

    try:
        send_email(data.email, reset_code)
    except:
        return response.resp_400(message="Send Email Failed")
    return response.resp_200(data=reset_code, message="Change Request Success")


@router.post("/password/forgot/reset", summary="reset pwd", description="reset pwd")
def pwd_reset_reset(data: user_schema.PwdResetReset, dal: UserDAL = Depends(DALGetter(UserDAL))):
    # error check
    if not data.reset_code_input == data.reset_code_generate:
        return response.resp_400(message="Wrong reset code")
    # if not User.password_check(data.password_1):
    #     return response.resp_400(message="Password invalid")
    if not User.verify_confirm_password(data.password_1, data.password_2):
        return response.resp_400(message="Different passwords")
    user = dal.get_by(email=data.email)
    # update password
    return response.resp_200(data=dal.update_password(data.password_1, user.id), message="Change Password Success")

