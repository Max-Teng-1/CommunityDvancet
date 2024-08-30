from pydantic import BaseModel


class Comment(BaseModel):
    campaign_id: int
    comment_text: str


class Get(BaseModel):
    comment_id: int


class GetByCampaign(BaseModel):
    campaign_id: int

class Update(BaseModel):
    comment_id: int
    content: str

