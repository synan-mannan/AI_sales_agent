import uvicorn
from app.config import settings
from app.scheduler import start_scheduler
from app.main import app
from app.utils import setup_logging

if __name__ == "__main__":
    setup_logging()
    start_scheduler()
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=False
    )
