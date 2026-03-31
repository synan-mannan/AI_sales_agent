import logging
import sys
from loguru import logger as loguru_logger

# Setup structlog or loguru
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
loguru_logger.add(sys.stdout, format="{time} {level} {message}", level="INFO")

def setup_logging():
    pass  # Advanced setup if needed
