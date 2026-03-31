from aiosmtpd.controller import Controller
from email.parser import BytesParser
import logging
from datetime import datetime, timedelta

import threading

import asyncio

from sqlalchemy import update

from app.crud import get_or_create_lead, create_email, get_or_create_conversation
from app.modules.ai_layer import classify_intent, generate_reply
from app.database import get_session

logger = logging.getLogger(__name__)


# ---------------------------
# EMAIL HANDLER
# ---------------------------
class EmailHandler:
    async def handle_DATA(self, server, session, envelope):
        try:
            bytes_msg = envelope.content
            msg = BytesParser().parsebytes(bytes_msg)

            # ✅ FIXED sender extraction
            sender = envelope.mail_from or msg.get("from") or "unknown@example.com"
            subject = msg.get("subject", "(no subject)")

            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode(errors="ignore")
                        break
            else:
                body = msg.get_payload(decode=True).decode(errors="ignore")

            await process_incoming_email(sender, subject, body)

            logger.info(f"Processed email from {sender}: {subject}")
            return "250 Message accepted"

        except Exception as e:
            import traceback
            logger.error(f"Error processing email: {e}")
            traceback.print_exc()
            return "550 Internal server error"


# ---------------------------
# SMTP SERVER
# ---------------------------
def start_mock_smtp(port: int = 1025):
    def run():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        handler = EmailHandler()

        controller = Controller(
            handler,
            hostname="127.0.0.1",
            port=port,
            ready_timeout=20  # increase timeout
        )

        controller.start()
        logger.info(f"Mock SMTP started on port {port}")

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            controller.stop()

    thread = threading.Thread(target=run, daemon=True)
    thread.start()

# ---------------------------
# EMAIL PROCESSING
# ---------------------------
async def process_incoming_email(sender_email: str, subject: str, body: str):
    async for db in get_session():  # ✅ correct async usage
        lead = await get_or_create_lead(db, sender_email)

        email_data = {
            "direction": "incoming",
            "subject": subject,
            "body": body,
        }

        email = await create_email(db, lead.id, email_data)

        # AI classification
        intent_data = await classify_intent(body)

        await db.execute(
            update(email.__class__)
            .where(email.__class__.id == email.id)
            .values(
                intent=intent_data["intent"],
                confidence=intent_data["confidence"],
            )
        )

        # Generate reply
        if intent_data["intent"] not in ["spam", "not_interested"]:
            reply = await generate_reply(lead, email, intent_data)

            await db.execute(
                update(email.__class__)
                .where(email.__class__.id == email.id)
                .values(response_body=reply)
            )

            print(f"SENDING REPLY TO {lead.email}: {reply[:100]}...")

        # Update conversation
        conv = await get_or_create_conversation(db, lead.id)
        conv.last_activity = datetime.utcnow()
        conv.next_fu_at = datetime.utcnow() + timedelta(days=3)