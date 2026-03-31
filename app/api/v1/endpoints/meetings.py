from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.dependencies import get_db
from app.schemas import MeetingCreate, MeetingResponse
from app.modules.meeting_scheduler import suggest_meeting_slots, schedule_meeting

router = APIRouter()

@router.get("/slots", response_model=List[dict])
async def get_meeting_slots(
    lead_id: int = Query(...),
    timezone: str = "UTC",
    db: AsyncSession = Depends(get_db)
):
    slots = await suggest_meeting_slots(lead_id, timezone)
    return slots

@router.post("/", response_model=MeetingResponse, status_code=201)
async def create_meeting_endpoint(meeting: MeetingCreate, db: AsyncSession = Depends(get_db)):
    return await schedule_meeting(meeting)
