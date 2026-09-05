from fastapi import APIRouter, Request, Response, HTTPException, status, Depends
from models.PostModels import PostsModel, PostCommentsModel, PostHeartModel, UpdatePostModel
from utils.database import database
from schemas.user_schema import CurrentUserSchema
from services.send_comment_services import send_comment_post
from services.add_post_services import add_post_user
from dependencies.get_posts_user import all_posts_users
from dependencies.get_current_user import get_current_user
from services.delete_post_services import deleting_post_user

posts_router = APIRouter()

@posts_router.post('/api/users/posts')
def add_post_in_public(response: Response, req_post: PostsModel):

    add_post_user(req_post=req_post)

    return HTTPException(status_code=status.HTTP_201_CREATED, detail="Successfully added new Post!") 

@posts_router.get('/api/users/posts')
async def get_all_posts_depends_audience(users_post = Depends(all_posts_users)):

    return HTTPException(status_code=status.HTTP_200_OK, detail=list(users_post))


@posts_router.post('/api/users/posts/comments')
def send_comment_in_post_user(user_req: PostCommentsModel):

    send_comment_post(user_req=user_req)

    return HTTPException(status_code=status.HTTP_201_CREATED, detail="Successfully Commented!")

@posts_router.post('/api/users/posts/hearts')
def heart_post_user(req_user: PostHeartModel):

    if req_user.isHeart:
        database.db_documents_users_posts.find_one_and_update({ "_id": req_user.id_post }, {
            "$inc": {
                "heart": 1
            }
        })
        return HTTPException(status_code=status.HTTP_200_OK, detail="Hearted!")
    else:
        database.db_documents_users_posts.find_one_and_update({ "_id": req_user.id_post }, {
            "$inc": {
                "heart": -1
            }
        })
        return HTTPException(status_code=status.HTTP_200_OK, detail="UnHeart!")

    
@posts_router.delete('/api/users/posts')
def delete_post_user(id_post: str, user: CurrentUserSchema = Depends(get_current_user)):

    deleting_post_user(id_post=id_post, user=user)

    return HTTPException(status_code=status.HTTP_200_OK, detail="Successfully deleted post!")

@posts_router.put("/api/users/posts")
def update_post_user(from_client: UpdatePostModel):

    user = get_current_user(id=from_client.user)

    founded_post_user = database.db_documents_users_posts.find_one_and_update({
        "$and": [
            { "_id": from_client.post }, 
            { "email": user["email"] }
        ]
    }, {
        "$set": {
            "title": from_client.title,
            "description": from_client.description,
            "audience": from_client.audience
        }
    })

    if founded_post_user == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can't update this post. Because this is not your!")

    return HTTPException(status_code=status.HTTP_201_CREATED, detail="Successfully Updated Post!")