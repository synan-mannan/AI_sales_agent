from groq import AsyncGroq
from app.config import settings
from typing import Dict
import json
import logging
from enum import Enum
from app.models import Intent

logger = logging.getLogger(__name__)

client = AsyncGroq(api_key=settings.groq_api_key) if settings.groq_api_key else None

class MockResponses(Enum):
    PRODUCT_INQUIRY = {"intent": Intent.PRODUCT_INQUIRY, "confidence": 0.9}
    PRICING_REQUEST = {"intent": Intent.PRICING_REQUEST, "confidence": 0.95}
    DEMO_REQUEST = {"intent": Intent.DEMO_REQUEST, "confidence": 0.92}

async def classify_intent(email_body: str) -> Dict:
    if settings.use_mock_ai or not client:
        # Simple keyword mock
        body_lower = email_body.lower()
        if 'price' in body_lower or 'cost' in body_lower:
            return MockResponses.PRICING_REQUEST.value
        elif 'demo' in body_lower:
            return MockResponses.DEMO_REQUEST.value
        elif 'product' in body_lower:
            return MockResponses.PRODUCT_INQUIRY.value
        return {"intent": Intent.FOLLOW_UP_NEEDED, "confidence": 0.8}
    
    prompt = f"""
    Classify the customer email intent. Respond ONLY with valid JSON:
    {{
      "intent": "product_inquiry|pricing_request|demo_request|follow_up_needed|not_interested|spam",
      "confidence": 0.XX
    }}
    
    Email: {email_body}
    """
    
    try:
        response = await client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        result = json.loads(response.choices[0].message.content)
        result['intent'] = Intent(result['intent'])
        return result
    except Exception as e:
        logger.error(f"AI classification error: {e}")
        return {"intent": Intent.FOLLOW_UP_NEEDED, "confidence": 0.5}

async def generate_reply(lead, email, intent_data: Dict) -> str:
    if settings.use_mock_ai or not client:
        templates = {
            Intent.PRODUCT_INQUIRY: f"Hi {lead.name or ''}, Thanks for your interest in our product...",
            Intent.PRICING_REQUEST: f"Hi {lead.name or ''}, Our pricing starts at $99/month...",
            Intent.DEMO_REQUEST: f"Hi {lead.name or ''}, Great! Let's schedule a demo. Reply with available times."
        }
        return templates.get(intent_data['intent'], "Thank you for your email. We'll get back to you soon.")
    
    prompt = f"""
    Generate professional sales reply for intent: {intent_data['intent']}
    Personalize for lead: {lead.name}, {lead.company}
    Email subject: {email.subject}
    Keep concise, call-to-action focused.
    """
    
    try:
        response = await client.chat.completions.create(
            model="llama3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Reply generation error: {e}")
        return "Thank you for your interest. A team member will reply soon."

