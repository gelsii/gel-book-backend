from pydantic import BaseModel

class SendMessageModel(BaseModel):
    message: str
    user_id: str
