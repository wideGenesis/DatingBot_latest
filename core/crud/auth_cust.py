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

from core import schemas
from config.conf import FAST_API_CONF
from core.tables import models
from db.engine import get_session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/sign-in/')


def get_current_user(token: str = Depends(oauth2_scheme)) -> schemas.User:
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
    def create_token(cls, user: models.Customer) -> schemas.Token:
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

    def register_new_user(
        self,
        user_data: schemas.UserCreate,
    ) -> schemas.Token:
        user = models.Customer(
            email=user_data.email,
            username=user_data.username,
            password_hash=self.hash_password(user_data.password),
        )
        self.session.add(user)
        self.session.commit()
        return self.create_token(user)

    def authenticate_user(
        self,
        username: str,
        password: str,
    ) -> schemas.Token:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

        user = (
            self.session
            .query(models.Customer)
            .filter(models.Customer.username == username)
            .first()
        )

        if not user:
            raise exception

        if not self.verify_password(password, user.password_hash):
            raise exception

        return self.create_token(user)


# import jwt
# from fastapi import HTTPException, Security
# from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
# from passlib.context import CryptContext
# from datetime import datetime, timedelta
#
#
# class AuthHandler():
#     security = HTTPBearer()
#     pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#     secret = 'SECRET'
#
#     def get_password_hash(self, password):
#         return self.pwd_context.hash(password)
#
#     def verify_password(self, plain_password, hashed_password):
#         return self.pwd_context.verify(plain_password, hashed_password)
#
#     def encode_token(self, user_id):
#         payload = {
#             'exp': datetime.utcnow() + timedelta(days=0, minutes=5),
#             'iat': datetime.utcnow(),
#             'sub': user_id
#         }
#         return jwt.encode(
#             payload,
#             self.secret,
#             algorithm='HS256'
#         )
#
#     def decode_token(self, token):
#         try:
#             payload = jwt.decode(token, self.secret, algorithms=['HS256'])
#             return payload['sub']
#         except jwt.ExpiredSignatureError:
#             raise HTTPException(status_code=401, detail='Signature has expired')
#         except jwt.InvalidTokenError as e:
#             raise HTTPException(status_code=401, detail='Invalid token')
#
#     def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
#         return self.decode_token(auth.credentials)