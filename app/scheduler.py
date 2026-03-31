from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.config import settings
from app.modules.follow_up import check_and_send_followups
from app.modules.email_ingestion import start_mock_smtp
import threading

scheduler = AsyncIOScheduler()
scheduler.add_job(
    check_and_send_followups, 
    'interval', 
    minutes=settings.followup_interval_minutes
)

def start_scheduler():
    scheduler.start()
    # Start SMTP in thread
    smtp_thread = threading.Thread(target=start_mock_smtp, args=(settings.email_mock_port,))
    smtp_thread.daemon = True
    smtp_thread.start()
