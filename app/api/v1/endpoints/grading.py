from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()

@router.post("/grade")
async def grade_submission():
    """
    Grade a student submission.
    Will be implemented when grading service is set up.
    """
    return {"message": "Not implemented yet"}
