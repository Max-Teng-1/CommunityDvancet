import time
import pytz

from jose import jwt
from datetime import datetime
from typing import Optional, Union, Any
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError

from src.backend.db.session import get_db
from src.backend.config import config
from src.backend.common import custom_exc
from src.backend.db.dals.user_dal import UserOtherDAL
from src.backend.routers.helper import *

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f'/factory/api/user/login/access_token/'
)


class DALGetter:
    def __init__(self, dal_cls):
        self.dal_cls = dal_cls

    def __call__(self):
        db = next(get_db())
        try:
            dal_instance = self.dal_cls(db_session=db)
            yield dal_instance
        finally:
            db.close()


def check_jwt_token(
        token: Optional[str] = Header(..., description="login token")
) -> Union[str, Any]:
    """
    check token
    default: check the token in headers
    :param token:
    :return:
    """

    try:
        payload = jwt.decode(
            token,
            config.SECRET_KEY, algorithms=[config.ALGORITHM]
        )
        # expired_time = time.strftime(str('%Y-%m-%d %H:%M:%S'), time.localtime(payload.get("exp")))
        # current_time = datetime_to_str(datetime.now(pytz.timezone('Australia/Sydney')))
        # print(expired_time)
        # print(current_time)

        return payload
    except jwt.ExpiredSignatureError:
        return None
        # raise custom_exc.TokenExpired()
    except (jwt.JWTError, ValidationError, AttributeError):
        raise custom_exc.TokenAuthError()

def get_user(
        payload: Optional[dict] = Depends(check_jwt_token)
):
    """
    get the current user by the user_id in token's payload
    :param db:
    :param token:
    :return:
    """
    if not payload:
        return None
    user = UserOtherDAL.get(user_id=payload.get("UserId"))
    
    return user

