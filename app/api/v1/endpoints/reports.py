from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()

@router.get("/generate")
async def generate_report():
    """
    Generate a report.
    Will be implemented when reporting service is set up.
    """
    return {"message": "Not implemented yet"}

@router.get("/{report_id}")
async def get_report(report_id: int):
    """
    Get a specific report by ID.
    Will be implemented when reporting service is set up.
    """
    return {"message": "Not implemented yet", "report_id": report_id}
