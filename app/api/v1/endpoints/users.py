from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()

@router.get("/me")
async def read_users_me():
    """
    Get current user.
    Will be implemented when authentication is set up.
    """
    return {"message": "Not implemented yet"}

@router.post("/")
async def create_user():
    """
    Create new user.
    Will be implemented when user management is set up.
    """
    return {"message": "Not implemented yet"}
