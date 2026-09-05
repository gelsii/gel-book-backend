from fastapi import HTTPException, status, Depends
from bson.objectid import ObjectId
from utils.database import database
from dependencies.get_current_user import get_current_user
from schemas.user_schema import CurrentUserSchema
from schemas.posts_schema import PostsSchema

http_exeption_getting_posts = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post is not found.")

def get_posts_using_find_by_id(id: str) -> PostsSchema:
    founded_posts = database.db_documents_users_posts.find_one({ "_id": id })

    if founded_posts == None:
        raise http_exeption_getting_posts

    return founded_posts

def get_all_posts_users_using_condition(condition: dict) -> PostsSchema:
    founded_posts = database.db_documents_users_posts.find(condition)

    if founded_posts == None:
        raise http_exeption_getting_posts

    return founded_posts


def all_posts_users(audience: str | None = None, condition: dict | None = None):
    users_post = database.db_documents_users_posts.find({ "audience": { "$ne": audience } })

    if condition:
        return database.db_documents_users_posts.find(condition)
    
    return users_post