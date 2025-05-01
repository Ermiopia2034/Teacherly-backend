from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()

@router.post("/record")
async def record_attendance():
    """
    Record attendance for a class.
    Will be implemented when attendance service is set up.
    """
    return {"message": "Not implemented yet"}

@router.get("/report")
async def get_attendance_report():
    """
    Get attendance report for a class or student.
    Will be implemented when attendance service is set up.
    """
    return {"message": "Not implemented yet"}
