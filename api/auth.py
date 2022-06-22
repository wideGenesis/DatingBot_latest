from fastapi import (
    APIRouter,
    Depends,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm

import schemas
from crud.auth import (
    AuthService,
    get_current_user,
)


router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)


@router.post(
    '/sign-up/',
    response_model=schemas.Token,
    status_code=status.HTTP_201_CREATED,
)
async def sign_up(
    user_data: schemas.UserCreate,
    auth_service: AuthService = Depends(),
):
    return await auth_service.register_new_user(user_data)


@router.post(
    '/sign-in/',
    response_model=schemas.Token,
)
async def sign_in(
    auth_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(),
):
    return await auth_service.authenticate_user(
        auth_data.username,
        auth_data.password,
    )


@router.get(
    '/user/',
    response_model=schemas.User,
)
async def get_user(user: schemas.User = Depends(get_current_user)):
    return user
