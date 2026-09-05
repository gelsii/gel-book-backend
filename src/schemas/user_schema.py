from pydantic import BaseModel

class CurrentUserSchema(BaseModel):
    username: str
    email: str
    _id: str
