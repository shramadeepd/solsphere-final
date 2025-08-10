import os
from typing import List

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8001")
API_ENDPOINT = os.getenv("API_ENDPOINT", "/api/v1/report")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))

# Check intervals (in minutes)
CHECK_INTERVAL_MINUTES = int(os.getenv("CHECK_INTERVAL_MINUTES", "30"))
MIN_CHECK_INTERVAL = 15  # Minimum 15 minutes
MAX_CHECK_INTERVAL = 60  # Maximum 60 minutes

# Ensure check interval is within bounds
if CHECK_INTERVAL_MINUTES < MIN_CHECK_INTERVAL:
    CHECK_INTERVAL_MINUTES = MIN_CHECK_INTERVAL
elif CHECK_INTERVAL_MINUTES > MAX_CHECK_INTERVAL:
    CHECK_INTERVAL_MINUTES = MAX_CHECK_INTERVAL

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "system_utility.log")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Retry Configuration
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
RETRY_DELAY = int(os.getenv("RETRY_DELAY", "5"))  # seconds

# System Information
MACHINE_ID_FILE = "machine_id.txt"
STATE_FILE = "last_state.json"

# Health Check Thresholds
DISK_ENCRYPTION_REQUIRED = True
ANTIVIRUS_REQUIRED = True
MAX_INACTIVITY_MINUTES = 10
MAX_OS_UPDATE_DAYS = 30
