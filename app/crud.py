from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models import Lead, Email, Conversation, Meeting
from app.schemas import LeadCreate, EmailProcess, MeetingCreate
from typing import List, Optional, Dict, Any

async def get_lead(session: AsyncSession, email: str) -> Optional[Lead]:
    result = await session.execute(select(Lead).where(Lead.email == email))
    return result.scalar_one_or_none()

async def create_lead(session: AsyncSession, lead: LeadCreate) -> Lead:
    db_lead = Lead(email=lead.email, name=lead.name, company=lead.company)
    session.add(db_lead)
    await session.flush()
    return db_lead

async def get_or_create_lead(session: AsyncSession, email: str, name: Optional[str] = None, company: Optional[str] = None) -> Lead:
    lead = await get_lead(session, email)
    if not lead:
        lead = await create_lead(session, LeadCreate(email=email, name=name, company=company))
    return lead

async def create_email(session: AsyncSession, lead_id: int, email_data: Dict[str, Any]) -> Email:
    db_email = Email(lead_id=lead_id, **email_data)
    session.add(db_email)
    await session.flush()
    return db_email

async def update_conversation(session: AsyncSession, lead_id: int, updates: Dict[str, Any]):
    stmt = update(Conversation).where(Conversation.lead_id == lead_id).values(**updates)
    await session.execute(stmt)

async def get_or_create_conversation(session: AsyncSession, lead_id: int) -> Conversation:
    result = await session.execute(select(Conversation).where(Conversation.lead_id == lead_id))
    conv = result.scalar_one_or_none()
    if not conv:
        conv = Conversation(lead_id=lead_id)
        session.add(conv)
        await session.flush()
    return conv

async def create_meeting(session: AsyncSession, meeting: MeetingCreate) -> Meeting:
    db_meeting = Meeting(**meeting.dict())
    session.add(db_meeting)
    await session.flush()
    return db_meeting

async def get_pending_followups(session: AsyncSession) -> List[Conversation]:
    stmt = select(Conversation).where(
        Conversation.next_fu_at < datetime.utcnow(),
        Conversation.stage != "converted"
    )
    result = await session.execute(stmt)
    return result.scalars().all()

async def get_leads(session: AsyncSession) -> List[Lead]:
    stmt = select(Lead).options(selectinload(Lead.conversations), selectinload(Lead.emails))
    result = await session.execute(stmt)
    return result.scalars().all()

from datetime import datetime  # Add for get_pending_followups
