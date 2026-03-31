from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional
from enum import Enum
from app.models import Intent, Direction, Stage, MeetingStatus

class IntentResponse(BaseModel):
    intent: Intent
    confidence: float = Field(..., ge=0.0, le=1.0)

class EmailProcess(BaseModel):
    sender_email: EmailStr
    subject: str
    body: str

class EmailResponse(BaseModel):
    id: int
    lead_id: Optional[int]
    direction: Direction
    subject: str
    intent: Optional[Intent]
    confidence: Optional[float]
    response_body: Optional[str]

class LeadCreate(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    company: Optional[str] = None

class LeadResponse(BaseModel):
    id: int
    email: EmailStr
    name: Optional[str]
    company: Optional[str]
    created_at: datetime

class ConversationResponse(BaseModel):
    id: int
    lead_id: int
    stage: Stage
    last_activity: datetime
    next_fu_at: Optional[datetime]

class MeetingCreate(BaseModel):
    lead_id: int
    email_id: Optional[int]
    time_slot: datetime
    timezone: str = "UTC"

class MeetingResponse(BaseModel):
    id: int
    lead_id: int
    time_slot: datetime
    status: MeetingStatus
    calendar_event_id: Optional[str]
