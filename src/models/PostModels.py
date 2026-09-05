from pydantic import BaseModel

class PostsModel(BaseModel):
    id: str
    audience: str
    title: str
    description: str

class PostCommentsModel(BaseModel):
    id_user: str
    id_post: str
    message: str

class PostHeartModel(BaseModel):
    id_post: str
    isHeart: bool


class UpdatePostModel(BaseModel):
    user: str
    post: str
    title: str
    description: str
    audience: str
