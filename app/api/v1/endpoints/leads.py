from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.dependencies import get_db
from app.schemas import LeadCreate, LeadResponse
from app.crud import get_leads, get_or_create_lead, create_lead

router = APIRouter()

@router.get("/", response_model=List[LeadResponse])
async def list_leads(db: AsyncSession = Depends(get_db)):
    leads = await get_leads(db)
    return leads

@router.post("/", response_model=LeadResponse, status_code=201)
async def create_lead_endpoint(lead: LeadCreate, db: AsyncSession = Depends(get_db)):
    existing = await get_lead(db, lead.email)
    if existing:
        raise HTTPException(status_code=400, detail="Lead exists")
    return await create_lead(db, lead)
