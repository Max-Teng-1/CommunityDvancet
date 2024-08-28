from typing import List, Dict
from pydantic import BaseModel


class AvailableTime(BaseModel):
    date_start: str
    date_end: str


class Approve(BaseModel):
    campaign_id: int

class Reject(BaseModel):
    campaign_id: int

