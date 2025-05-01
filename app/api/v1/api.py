from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, content_generation, grading, students, attendance, reports, settings

# Create main v1 router
router = APIRouter()

# Include all endpoint routers
# These will be implemented as we develop each feature
# For now, they're commented out to avoid import errors
# router.include_router(auth.router, prefix="/auth", tags=["authentication"])
# router.include_router(users.router, prefix="/users", tags=["users"])
# router.include_router(content_generation.router, prefix="/content", tags=["content"])
# router.include_router(grading.router, prefix="/grading", tags=["grading"])
# router.include_router(students.router, prefix="/students", tags=["students"])
# router.include_router(attendance.router, prefix="/attendance", tags=["attendance"])
# router.include_router(reports.router, prefix="/reports", tags=["reports"])
# router.include_router(settings.router, prefix="/settings", tags=["settings"])
