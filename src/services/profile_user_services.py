from fastapi import HTTPException, status
from schemas.user_schema import CurrentUserSchema
from dependencies.get_posts_user import all_posts_users


def get_profile_info_user(user: CurrentUserSchema):
    http_exeption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized...")
    
    founded_all_posts_user = list(all_posts_users(condition={ "email": user['email']}))

    if founded_all_posts_user == None:
        raise http_exeption

    posts_user_and_username = {
        "username": user['username'],
        "posts": founded_all_posts_user
    }

    return posts_user_and_username