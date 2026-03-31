from fastapi import APIRouter
from .endpoints import leads, emails, followups, meetings

api_router = APIRouter()

api_router.include_router(leads.router, prefix="/leads", tags=["leads"])
api_router.include_router(emails.router, prefix="/emails", tags=["emails"])
api_router.include_router(followups.router, prefix="/followups", tags=["followups"])
api_router.include_router(meetings.router, prefix="/meetings", tags=["meetings"])
