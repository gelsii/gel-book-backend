from fastapi import APIRouter, Request, Response, HTTPException, status, Depends
from fastapi.responses import RedirectResponse
from fastapi.security import APIKeyCookie
from models.UserModel import UserModelSignIn, UserModels
from utils.database import database
from utils.token import authenticate_access_token_user
from bson.objectid import ObjectId
from services.sign_in_services import authenticate_user_signing_in
from services.sign_up_services import authenticate_sign_up_user
from services.auth_access_page_services import is_valid_access_auth_page
from utils.token import generate_access_token, token_expire_minutes
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from dependencies.get_current_user import get_current_user

load_dotenv

auth_router = APIRouter()

@auth_router.post('/api/users/signup')
def sign_up_user(client_req: UserModels):
    authenticate_sign_up_user(client_req=client_req)

    return HTTPException(status_code=status.HTTP_201_CREATED, detail="Successfully Sign Up! You can now Sign In!")

@auth_router.post('/api/users/signin')
def sign_in_user(response: Response, client_req: UserModelSignIn):

    authenticate_user_signing_in(response=response,client_req=client_req)

    return HTTPException(status_code=status.HTTP_202_ACCEPTED, detail="Welcome!")


@auth_router.post('/api/users/access')
def authorize_user(request: Request, user = Depends(authenticate_access_token_user)):

    return HTTPException(status_code=status.HTTP_202_ACCEPTED, detail={ "message": "Welcome!", "user": user['payload']['_id'] })

key_cookie_req_access_token = APIKeyCookie(name="access_token")

@auth_router.get('/api/users/logout')
def logout_user(response: Response, token = Depends(key_cookie_req_access_token)):

    decoded_token = authenticate_access_token_user(token=token)

    database.db_documents_tokens_expired.insert_one({ 
        "token": token,
        "expire_date": decoded_token["payload"]["exp"]
    })

    response.delete_cookie(key="access_token", secure=True, httponly=True, domain="localhost")

    return HTTPException(status_code=status.HTTP_202_ACCEPTED, detail="Successfully logout!")

@auth_router.get('/api/users/settings')
def get_info_user(user = Depends(get_current_user)):
    
    detail_user = {
        "username": user["username"],
        "email": user["email"],
        "password": f"".ljust(15, "*")
    }

    return HTTPException(status_code=status.HTTP_202_ACCEPTED, detail=detail_user)

# @auth_router.get('/api/users/auth/page')
# def check_user_is_logged(response: Response):
#     generated_token = generate_access_token({ "access": True }, os.getenv("PRIVATE_ACCESS_AUTH_KEY"))

#     expiration_date_cookie = datetime.utcnow() + timedelta(minutes=token_expire_minutes)

#     response.set_cookie(key="auth", value=generated_token["access_token"], expires=f'{expiration_date_cookie}', httponly=True, secure=True, path="/")

# key_cookie_req_auth = APIKeyCookie(name="auth")

# @auth_router.post('/api/users/auth/page/access')
# def authorize_user(token_access_page = Depends(key_cookie_req_auth)):
#     print(token_access_page)
#     decoded_token = authenticate_access_token_user(key=os.getenv("PRIVATE_ACCESS_AUTH_KEY"), token=token_access_page)

#     return HTTPException(status_code=status.HTTP_202_ACCEPTED, detail={ "message": "Welcome!", "access": decoded_token['payload']['access'] })
    
    