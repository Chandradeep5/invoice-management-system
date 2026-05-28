
import logging
import os

# Create logs folder if not exists
if not os.path.exists("logs"):
    os.makedirs("logs")

# Configure logger
logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
