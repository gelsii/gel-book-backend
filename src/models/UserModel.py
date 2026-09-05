from pydantic import BaseModel
from typing import Annotated

class UserModels(BaseModel):
    username: str
    email: str
    password: str

class UserModelSignIn(BaseModel):
    email: str
    password: str