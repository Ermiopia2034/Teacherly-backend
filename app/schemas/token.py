from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    """
    Token schema for API responses.
    """
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """
    Token payload schema for decoded JWT tokens.
    """
    sub: Optional[str] = None
    exp: Optional[int] = None
