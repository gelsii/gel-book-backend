from utils.database import database
from bson.objectid import ObjectId
from fastapi import HTTPException, status
from schemas.user_schema import CurrentUserSchema

def get_current_user(id: str) -> CurrentUserSchema:
    founded_user = database.db_documents_user.find_one({ "_id": ObjectId(id) }, { "password": 0 })

    if founded_user == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials.... Please Sign Up first.")

    return founded_user