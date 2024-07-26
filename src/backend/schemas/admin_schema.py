from typing import List, Dict
from pydantic import BaseModel


class AvailableTime(BaseModel):
    date_start: str
    date_end: str


class NotificationCreate(BaseModel):
    car_space_no: str










