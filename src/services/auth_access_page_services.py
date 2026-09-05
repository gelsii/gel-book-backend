from fastapi import HTTPException, status,Response, Depends
from fastapi.security import APIKeyCookie
from utils.encryption import decrypt_text
import jwt
from dotenv import load_dotenv
import os
from utils.token import authenticate_access_token_user

load_dotenv()

security_cookie_request = APIKeyCookie(name="access")

def is_valid_access_auth_page(is_access = Depends(security_cookie_request)):
    return is_access