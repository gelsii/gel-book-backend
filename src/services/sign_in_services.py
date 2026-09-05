from fastapi import Response, HTTPException, status
from models.UserModel import UserModelSignIn
import bcrypt
from utils.database import database
from utils.token import generate_access_token, token_expire_minutes
from datetime import datetime, timedelta
from utils.encryption import encrypt_private_word
import os
from dotenv import load_dotenv

load_dotenv()

def authenticate_user_signing_in(response: Response, client_req: UserModelSignIn):
    user_failed_exeption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password... Please check again.")
    
    user_founded = database.db_documents_user.find_one({ "email": client_req.email })

    if user_founded == None:
        raise user_failed_exeption

    is_match_password = bcrypt.checkpw(client_req.password.encode(), user_founded['password'])

    if not is_match_password:
        raise user_failed_exeption

    expiration_date_cookie = datetime.utcnow() + timedelta(minutes=token_expire_minutes)

    generated_token = generate_access_token({  "_id": str(user_founded['_id']) }, key=os.getenv("PRIVATE_ACCESS_TOKEN_KEY"))

    response.set_cookie(key="access_token", value=generated_token["access_token"], expires=f'{expiration_date_cookie}', httponly=True, secure=True, path="/", samesite="none")
    