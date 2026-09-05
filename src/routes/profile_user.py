from fastapi import APIRouter, HTTPException, status, Depends
from dependencies.get_current_user import get_current_user
from schemas.user_schema import CurrentUserSchema
from services.profile_user_services import get_profile_info_user

profile_router = APIRouter()

@profile_router.get('/api/users/profile')
def get_profie_info_user(user: CurrentUserSchema = Depends(get_current_user)):
    all_info_response_user = get_profile_info_user(user=user)

    return HTTPException(status_code=status.HTTP_200_OK, detail=all_info_response_user)

    