from fastapi import HTTPException, status
from utils.database import database
from schemas.user_schema import CurrentUserSchema

def deleting_post_user(id_post: str, user: CurrentUserSchema):
    founded_post_user = database.db_documents_users_posts.find_one_and_delete({
        "$and": [
            {"_id": id_post}, 
            {"email": user["email"]}
        ]
    })

    if founded_post_user == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can't delete this post. Because this is not your own!")
