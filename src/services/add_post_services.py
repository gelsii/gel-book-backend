from fastapi import HTTPException, status
from models.PostModels import PostsModel
from utils.database import database
from bson.objectid import ObjectId


def add_post_user(req_post: PostsModel):
    http_exeption_fields = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Fields... Please check again.")
    
    if req_post.description.rstrip() == "" or req_post.title.rstrip() == "":
        raise http_exeption_fields

    user_post_founded = database.db_documents_user.find_one({ "_id": ObjectId(req_post.id) })

    post_context = { 
        "_id": str(ObjectId()),
        "email": user_post_founded['email'],
        "title": req_post.title,
        "description": req_post.description,
        "comments": [],
        "heart": 0,
        "audience": req_post.audience
    }

    # match req_post.audience:
    #     case "private":
    #         database.db_documents_user.find_one_and_update({ "email": user_post_founded['email'] }, {
    #             "$push": {
    #                 "posts": post_context
    #             }
    #         }) 
    #     case "public":
    #         database.db_documents_users_posts.insert_one(post_context)
    #     case _:
    #         raise http_exeption_fields
    database.db_documents_users_posts.insert_one(post_context)