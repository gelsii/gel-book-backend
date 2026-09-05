from pydantic import BaseModel

class PostsSchema:
    _id: str
    email: str
    title: str
    description:str
    comments: list
    hearts: int