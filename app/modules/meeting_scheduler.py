from datetime import datetime, timedelta
from typing import List, Dict
from app.crud import get_leads, create_meeting
from app.database import get_session
from app.schemas import MeetingCreate
import random
from zoneinfo import ZoneInfo
import logging

logger = logging.getLogger(__name__)

class MockCalendar:
    @staticmethod
    def get_available_slots(lead_id: int, timezone: str = 'UTC', num_slots: int = 3) -> List[datetime]:
        now = datetime.now(ZoneInfo(timezone))
        slots = []
        for i in range(1, 8, 2):
            candidate = now + timedelta(days=i, hours=10 + random.randint(0, 6))
            slots.append(candidate)
        return slots[:num_slots]

    @staticmethod
    async def check_conflict(db_session, lead_id: int, time_slot: datetime) -> bool:
        # Query existing meetings
        # Impl: select count(*) where lead_id and overlapping time_slot
        return random.choice([False, False])  # Mock no conflict

async def suggest_meeting_slots(lead_id: int, timezone: str = 'UTC') -> List[Dict]:
    slots = MockCalendar.get_available_slots(lead_id, timezone)
    available = []
    async with get_session() as db:
        for slot in slots:
            if not await MockCalendar.check_conflict(db, lead_id, slot):
                available.append({'time_slot': slot.isoformat(), 'status': 'available'})
    return available

async def schedule_meeting(meeting: MeetingCreate):
    async with get_session() as db:
        # Check conflict
        if await MockCalendar.check_conflict(db, meeting.lead_id, meeting.time_slot):
            raise ValueError("Time slot conflict")
        db_meeting = await create_meeting(db, meeting)
        # Mock calendar event
        db_meeting.calendar_event_id = f"mock_{db_meeting.id}"
        return db_meeting
