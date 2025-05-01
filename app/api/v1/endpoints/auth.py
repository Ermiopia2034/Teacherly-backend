from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/login/access-token")
async def login_access_token():
    """
    OAuth2 compatible token login, get an access token for future requests.
    Will be implemented when authentication is set up.
    """
    return {"message": "Not implemented yet"}
