from fastapi import APIRouter, HTTPException, status, Depends
from utils.database import database
from dependencies.get_current_user import get_current_user
from models.ChatModels import SendMessageModel

chat_router = APIRouter()

@chat_router.get("/api/users/global-chats")
def get_all_chats_users(id: str):
    founded_user = get_current_user(id)

    # database.db_documents_global_chats.update_many({ "username": { "$ne": founded_user["username"] } }, {
    #     "$set": {
    #         "align": "start"
    #     }
    # })

    # database.db_documents_global_chats.update_many({ "username": { "$eq": founded_user["username"] } }, {
    #         "$set": {
    #             "align": "end"
    #         }
    #     })

    founded_all_chats = database.db_documents_global_chats.find({ }, { "_id": 0 })

    return HTTPException(status_code=status.HTTP_200_OK, detail=list(founded_all_chats))

@chat_router.post("/api/users/global-chats")
def send_message_to_global_chat(from_client: SendMessageModel ):
    founded_user = get_current_user(from_client.user_id)
    
    insert_message_prepare = {
        "username": founded_user["username"],
        "align": "end",
        "message": from_client.message
    }

    database.db_documents_global_chats.insert_one(insert_message_prepare)

    return HTTPException(status_code=status.HTTP_201_CREATED, detail="Sended Message!")