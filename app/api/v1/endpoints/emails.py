from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db
from app.schemas import EmailProcess, EmailResponse
from app.modules.email_ingestion import process_incoming_email

router = APIRouter()

@router.post("/process", response_model=EmailResponse)
async def process_email(email_data: EmailProcess, db: AsyncSession = Depends(get_db)):
    # Call ingestion logic
    await process_incoming_email(email_data.sender_email, email_data.subject, email_data.body)
    # Fetch and return latest email for lead
    lead = await get_or_create_lead(db, email_data.sender_email)
    # Impl get_latest_email for lead
    # Return mock
    return EmailResponse(
        id=1, 
        lead_id=lead.id,
        direction="incoming",
        subject=email_data.subject,
        body=email_data.body
    )
