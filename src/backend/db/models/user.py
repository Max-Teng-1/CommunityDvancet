import re
import pytz
from datetime import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy import Column, String, VARCHAR, Integer, DECIMAL, BOOLEAN
from passlib.context import CryptContext

from src.backend.db.models.base import Base
from src.backend.config import config


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class User(Base):
    __tablename__ = 'user'

    email = Column(VARCHAR(36), unique=True)
    password = Column(VARCHAR(128))
    first_name = Column(VARCHAR(50), default="new")
    last_name = Column(VARCHAR(50), default="user")
    role = Column(Integer, default=config.NORMAL_USER)
    avatar = Column(VARCHAR(128), default="src/backend/static/userAvatar/default.png")
    phone = Column(String(10), default="0400000000")
    recent_log = Column(VARCHAR(4096), default = "")

    is_locked = Column(BOOLEAN, default=False)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        :param plain_password
        :param hashed_password
        :return:

        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        :param password:
        :return:
        """
        return pwd_context.hash(password)

    @staticmethod
    def verify_email_regex(email: str):
        """
         :param email
         :return:
        """
        return re.fullmatch(config.EMAIL_REGEX, email)

    @staticmethod
    def verify_confirm_password(password_1: str, password_2: str):
        return password_1 == password_2

    @staticmethod
    def password_check(passwd):
        return any(char.isdigit() for char in passwd) and any(char.isupper() for char in passwd) and any(char.islower() for char in passwd) and any(char in config.SpecialSym for char in passwd) and len(passwd) >= 8

    @staticmethod
    def verify_phone(phone: str):
        return len(phone) == 10 and phone.isdigit() and phone[0] == '0' and phone[1] == '4'
    
    @staticmethod
    def verify_first_last_name(first_name: str, last_name: str):
        return 1 <= len(first_name.replace(" ", "")) <= 50 and 1 <= len(last_name.replace(" ", "")) <= 50

    # @staticmethod
    # def get_syd_time_after_4_month_str() -> str:
    #     return (datetime.now(pytz.timezone("Australia/Sydney"))+relativedelta(months=config.RESET_POINTS_MONTH)).strftime("%Y-%m-%d %H:%M:%S")

