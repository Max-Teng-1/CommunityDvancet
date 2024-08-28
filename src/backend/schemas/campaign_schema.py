from pydantic import BaseModel


class Campaign(BaseModel):
    title: str
    description: str
    image: str = None

class Get(BaseModel):
    campaign_id: int

class Update(BaseModel):
    campaign_id: int
    title: str
    description: str
    image: str = None

class Approve(BaseModel):
    campaign_id: int

class Reject(BaseModel):
    campaign_id: int

class Delete(BaseModel):
    campaign_id: int