import jwt
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Request, Depends, Response
from fastapi.security import APIKeyCookie, HTTPBearer, HTTPAuthorizationCredentials
from utils.database import database
from utils.encryption import encrypt_private_word, decrypt_text

load_dotenv()

security_key_cookie = APIKeyCookie(name="access_token")
private_access_token_key = os.getenv('PRIVATE_ACCESS_TOKEN_KEY')
token_expire_minutes = 30

def generate_access_token(additional_info: dict, key):
    expiration_date_access_token = datetime.utcnow() + timedelta(minutes=token_expire_minutes)

    try:
        generated_token = jwt.encode(
            payload={"exp": expiration_date_access_token, **additional_info },
            key=key, 
            algorithm="HS256")
    except Exception as error:
        print(error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error.")

    encrypted_token = encrypt_private_word(text=generated_token)

    return { "access_token": encrypted_token }


def authenticate_access_token_user(key: str = private_access_token_key, token: str = Depends(security_key_cookie)):
    token_exeption = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to this page.")

    database.db_documents_tokens_expired.delete_many({ "expire_date": { "$lte": int(datetime.now().timestamp()) } })

    founded_token = database.db_documents_tokens_expired.find_one({ "token": token })

    decrypted_token = decrypt_text(token)

    if founded_token != None:
        raise token_exeption

    try:
        decoded_token = jwt.decode(jwt=decrypted_token, key=key, algorithms=["HS256"])

        return { "payload": decoded_token }
    except jwt.InvalidTokenError:
        raise token_exeption
    except jwt.ExpiredSignatureError:
        raise token_exeption
    except Exception as error:
        print(error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error)

    
