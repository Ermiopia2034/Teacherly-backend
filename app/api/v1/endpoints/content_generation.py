from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()

@router.post("/generate")
async def generate_content():
    """
    Generate educational content.
    Will be implemented when content generation service is set up.
    """
    return {"message": "Not implemented yet"}
