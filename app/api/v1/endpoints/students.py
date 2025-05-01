from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()

@router.get("/")
async def list_students():
    """
    List all students.
    Will be implemented when student management is set up.
    """
    return {"message": "Not implemented yet"}

@router.post("/")
async def create_student():
    """
    Create a new student.
    Will be implemented when student management is set up.
    """
    return {"message": "Not implemented yet"}

@router.get("/{student_id}")
async def get_student(student_id: int):
    """
    Get a specific student by ID.
    Will be implemented when student management is set up.
    """
    return {"message": "Not implemented yet", "student_id": student_id}
