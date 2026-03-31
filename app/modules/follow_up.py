from app.crud import get_pending_followups, update_conversation, get_leads
from app.database import get_session
from app.modules.ai_layer import generate_reply
from app.models import Stage, Conversation
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

async def check_and_send_followups():
    async with get_session() as db:
        pending = await get_pending_followups(db)
        for conv in pending:
            if conv.stage == Stage.INITIAL:
                reply = "Hi, following up on my previous email. Any questions?"
                conv.stage = Stage.FU1
            elif conv.stage == Stage.FU1:
                reply = "Quick follow-up. Still interested?"
                conv.stage = Stage.FU2
            else:
                reply = "Last attempt. Let me know if interested!"
                conv.stage = Stage.CLOSED
            
            await update_conversation(db, conv.lead_id, {
                'stage': conv.stage,
                'last_activity': datetime.utcnow(),
                'next_fu_at': None if conv.stage == Stage.CLOSED else datetime.utcnow() + timedelta(days=7)
            })
            
            lead = await get_lead(db, ...)  # Impl get_lead from lead.email if needed
            print(f"FOLLOW-UP SENT for lead {conv.lead_id}: {reply[:100]}...")
            logger.info(f"Sent follow-up for lead_id={conv.lead_id}, stage={conv.stage}")
    
    logger.info("Follow-up check complete")

# Note: Expand with actual lead fetch for personalized reply
