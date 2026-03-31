from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.dependencies import get_db
from app.crud import get_pending_followups
from app.schemas import ConversationResponse

router = APIRouter()

@router.get("/pending", response_model=List[ConversationResponse])
async def get_pending_followups_endpoint(db: AsyncSession = Depends(get_db)):
    pending = await get_pending_followups(db)
    return pending

@router.post("/send-all")
async def send_all_pending(db: AsyncSession = Depends(get_db)):
    await check_and_send_followups()  # From modules
    return {"status": "sent"}
