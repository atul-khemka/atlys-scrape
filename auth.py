from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

from settings import Settings

header_scheme = APIKeyHeader(name="token")

def check_token(token: str = Depends(header_scheme)):
    settings = Settings()
    if token != settings.token:
        raise HTTPException(status_code=401, detail="Unauthorized access")