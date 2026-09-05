from fastapi import HTTPException, status
from models.UserModel import UserModels
import bcrypt
from utils.database import database
from utils.encryption import encrypt_private_word, decrypt_text

def authenticate_sign_up_user(client_req: UserModels):
    requested_from_client = client_req
    
    user_founded_same_info = database.db_documents_user.find_one({ "email": requested_from_client.email })

    if user_founded_same_info != None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="already sign in this email.")

    if requested_from_client.username.strip() == "" or requested_from_client.email.strip() == "" or requested_from_client.password.rstrip() == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid fields... Please check again.")
    
    salt = bcrypt.gensalt(12)

    hashed_password = bcrypt.hashpw(requested_from_client.password.encode(), salt)

    created_user = {
        "username": requested_from_client.username,
        "email": requested_from_client.email,
        "password": hashed_password,
        "posts": []
    }

    database.db_documents_user.insert_one(document=created_user)