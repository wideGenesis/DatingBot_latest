from fastapi import Security, HTTPException, Depends

from settings.conf import FAST_API_CONF
from passlib.context import CryptContext
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN


class ApiKeyService:
    @classmethod
    async def get_api_key(
        cls,
        _api_key_query: str = Security(
            APIKeyQuery(name="access_token", auto_error=False)
        ),
        # _api_key_header: str = Security(APIKeyHeader(name="access_token", auto_error=False)),
        # _api_key_cookie: str = Security(APIKeyCookie(name="access_token", auto_error=False)),
    ):
        if _api_key_query == FAST_API_CONF.SECRET:
            return _api_key_query
        # elif _api_key_header == FAST_API_CONF.SECRET:
        #     return _api_key_header
        # elif _api_key_cookie == FAST_API_CONF.SECRET:
        #     return _api_key_cookie
        else:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
            )
