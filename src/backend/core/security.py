from src.backend.config import config
import time
import pytz

from typing import Any, Union, Optional
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from src.backend.routers.helper import *
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def create_access_token(user_id: Union[str, Any], user_role: Union[str, int], expires_delta: timedelta = None) -> str:
    """
    :param user_id:
    :param user_role: permission
    :param expires_delta
    :return:
    """

    if expires_delta:
        expire = datetime.now(pytz.timezone('Australia/Sydney')) + expires_delta
    else:
        expire = datetime.now(pytz.timezone('Australia/Sydney')) + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"user_id": user_id, "user_role": user_role, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt

def create_security_key(expires_delta: timedelta = None) -> str:
    """
    :param expires_delta
    :return:
    """

    if expires_delta:
        expire = datetime.now(pytz.timezone('Australia/Sydney')) + expires_delta
    else:
        expire = datetime.now(pytz.timezone('Australia/Sydney')) + timedelta(minutes=config.SECURITY_KEY_EXPIRE_MINUTES)
    to_encode = {"exp": expire}
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt

def check_security_key(security_key: str) -> Union[str, Any]:
    try:
        payload = jwt.decode(
            security_key,
            config.SECRET_KEY, algorithms=[config.ALGORITHM]
        )

        expired_time = time.strftime(str('%Y-%m-%d %H:%M:%S'), time.localtime(payload.get("exp")))
        current_time = datetime_to_str(datetime.now(pytz.timezone('Australia/Sydney')))
        return True
    except jwt.ExpiredSignatureError:
        return False
        # raise custom_exc.TokenExpired()

