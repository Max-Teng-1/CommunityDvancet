from typing import Optional
from pydantic import BaseSettings
from functools import lru_cache



class Config(BaseSettings):
    # database setting
    MYSQL_USERNAME: str = "testuser"
    MYSQL_PASSWORD: str = "Allen123456"
    MYSQL_HOST: str = "1.2.3.4"
    MYSQL_PORT: int = 3306
    MYSQL_DATABASE: str = "testdb"

    # api setting
    DEBUG: bool = True
    TITLE: str = "CommunityDvancet"
    DESCRIPTION: str = "CommunityDvancet"
    DOCS_URL: str = "/docs"
    OPENAPI_URL: str = "/api/openapi.json"
    REDOC_URL: Optional[str] = "/api/redoc"

    # user role
    NORMAL_USER: int = 1
    ADMIN: int = 2
    SUPER_ADMIN: int = 3

    # backend host and port (should be different from mysql host and port)
    PORT: int = 8000
    HOST: str = "0.0.0.0"

    # token expired time
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 7 * 24 * 60
    # security key expired time
    SECURITY_KEY_EXPIRE_MINUTES: int = 15

    # password encode setting
    SECRET_KEY: str = 'Allen'
    ALGORITHM: str = 'HS256'

    # email regex
    EMAIL_REGEX: str = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'

    # special symbol
    SpecialSym = ["!", "@", "#", "$", "%", "^", "&", "*", ",", ".", "?", "/", "[", "]", "~", "`", "|", ":", ";", "-", "_", "+", "="]

    # uuid length
    DIGITS: int = 6

    # state codes for search
    state_abbreviation = {'NSW': 'New South Wales','QLD': 'Queensland','WA': 'Western Australia','SA': 'South Australia','NT': 'Northern Territory','VIC': 'Victoria','ACT': 'Australian Capital Territory','TAS': 'Tasmania'}
    city_codes = ["Sydney NSW, Australia", "Sydney New South Wales, Australia", "Brisbane QLD, Australia", "Brisbane Queensland, Australia", "Perth WA, Australia", "Perth Western Australia, Australia", "Adelaide SA, Australia", "Adelaide South Australia, Australia", "Darwin NT, Australia", "Darwin Northern Territory, Australia", "Melbourne Victoria, Australia",  "Melbourne VIC, Australia", "Canberra ACT, Australia", "Canberra Australian Capital Territory, Australia", "Hobart TAS, Australia", "Hobart Tasmania, Australia", "Sydney NSW 2000, Australia", "Sydney New South Wales 2000, Australia", "Brisbane QLD 4000, Australia", "Brisbane Queensland 4000, Australia", "Perth WA 6000, Australia", "Perth Western Australia 6000, Australia", "Adelaide SA 5000, Australia", "Adelaide South Australia 5000, Australia", "Darwin NT 0800, Australia", "Darwin Northern Territory 0800, Australia", "Melbourne Victoria 3000, Australia",  "Melbourne VIC 3000, Australia", "Canberra ACT 2600, Australia", "Canberra Australian Capital Territory 2600, Australia", "Hobart TAS 7000, Australia", "Hobart Tasmania 7000, Australia", "2000", "2600", "3000", "4000", "5000", "6000", "7000", "0800"]

    # user avatar path
    USER_AVATAR_PATH: str = "src/backend/static/userAvatar/"

    # test url
    TEST_URL: str = f"http://{HOST}:{PORT}/"


@lru_cache()
def get_config():
    return Config()

config = get_config()
