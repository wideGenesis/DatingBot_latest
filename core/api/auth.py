from fastapi import (
    APIRouter,
    Depends,
    status,
    HTTPException
)
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

security = HTTPBasic()
# from core.schemas.auth import Token, UserCreate, User
# from core.crud.auth import (
#     AuthService,
# get_current_user,
# )

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


async def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "stanleyjobson")
    correct_password = secrets.compare_digest(credentials.password, "swordfish")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@router.get(
    "/sign-in/",
    # response_model=Token,
)
async def sign_in(username: str = Depends(get_current_username)):
    return {"username": username, 'access': 'allowed'}

# @router.post(
#     '/sign-up/',
#     response_model=Token,
#     status_code=status.HTTP_201_CREATED,
# )
# def sign_up(
#     user_data: UserCreate,
#     auth_service: AuthService = Depends(),
# ):
#     return auth_service.register_new_user(user_data)

# @router.get(
#     '/user/',
#     response_model=User,
# )
# def get_user(user: User = Depends(get_current_user)):
#     return user


# auth_handler = AuthHandler()
# users = []
#
#
# @app.post('/register', status_code=201)
# def register(auth_details: AuthDetails):
#     if any(x['username'] == auth_details.username for x in users):
#         raise HTTPException(status_code=400, detail='Username is taken')
#     hashed_password = auth_handler.get_password_hash(auth_details.password)
#     users.append({
#         'username': auth_details.username,
#         'password': hashed_password
#     })
#     return
#
#
# @app.post('/login')
# def login(auth_details: AuthDetails):
#     user = None
#     for x in users:
#         if x['username'] == auth_details.username:
#             user = x
#             break
#
#     if (user is None) or (not auth_handler.verify_password(auth_details.password, user['password'])):
#         raise HTTPException(status_code=401, detail='Invalid username and/or password')
#     token = auth_handler.encode_token(user['username'])
#     return {'token': token}
#
#
# @app.get('/unprotected')
# def unprotected():
#     return {'hello': 'world'}
#
#
# @app.get('/protected')
# def protected(username=Depends(auth_handler.auth_wrapper)):
#     return {'name': username}
