from datetime import (
    datetime,
    timedelta,
)

from fastapi import (
    Depends,
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordBearer
from jose import (
    JWTError,
    jwt,
)
from passlib.hash import bcrypt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from core.tables import models
from core import schemas

from db.engine import get_session
from settings.conf import FAST_API_CONF
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

security = HTTPBasic()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/sign-in/')


async def get_current_user(token: str = Depends(oauth2_scheme)) -> schemas.User:
    return AuthService.verify_token(token)


class AuthService:
    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    def verify_token(cls, token: str) -> schemas.User:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
        try:
            payload = jwt.decode(
                token,
                FAST_API_CONF.JWT_SECRET,
                algorithms=[FAST_API_CONF.JWT_ALGO],
            )
        except JWTError:
            raise exception from None

        user_data = payload.get('user')

        try:
            user = schemas.User.parse_obj(user_data)
        except ValidationError:
            raise exception from None

        return user

    @classmethod
    async def create_token(cls, user: models.User) -> schemas.Token:
        user_data = schemas.User.from_orm(user)
        now = datetime.utcnow()
        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(seconds=FAST_API_CONF.JWT_EXPIRES_S),
            'sub': str(user_data.id),
            'user': user_data.dict(),
        }

        token = jwt.encode(
            payload,
            FAST_API_CONF.JWT_SECRET,
            algorithm=FAST_API_CONF.JWT_ALGO,
        )

        return schemas.Token(access_token=token)

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    async def register_new_user(
        self,
        user_data: schemas.UserCreate,
    ) -> schemas.Token:

        user = models.User(
            email=user_data.email,
            username=user_data.username,
            password_hash=self.hash_password(user_data.password),
        )
        await user.save()
        return await self.create_token(user)

    async def authenticate_user(
        self,
        username: str,
        password: str,
    ) -> schemas.Token:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

        user = await models.User.objects.get_or_none(username=username)

        if not user:
            raise exception

        if not self.verify_password(password, user.password_hash):
            raise exception

        return await self.create_token(user)

    async def authenticate_service(
        self, credentials: HTTPBasicCredentials = Depends(security)
    ):

        correct_username = secrets.compare_digest(credentials.username, "adm-bot")
        correct_password = secrets.compare_digest(credentials.password, "general2035")
        if not (correct_username and correct_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="UNAUTHORIZED REQUEST",
                headers={"WWW-Authenticate": "Basic"},
            )
        return True
