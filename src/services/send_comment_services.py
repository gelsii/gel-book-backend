from fastapi import HTTPException, status, Depends
from models.PostModels import PostCommentsModel
from utils.database import database
from bson.objectid import ObjectId
from dependencies.get_current_user import get_current_user

def send_comment_post(user_req: PostCommentsModel):
    request_info = user_req

    user_founded = get_current_user(user_req.id_user)
    
    final_output_comment = {
        "_id": str(ObjectId()),
        "username": user_founded["username"],
        "message": request_info.message,
        "replyes": [],
    }

    user_posts_founded = database.db_documents_users_posts.find_one_and_update({ "_id": request_info.id_post }, {
        "$push": {
            "comments": final_output_comment 
        }
    })

    if user_posts_founded == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="404 - Not found post.")