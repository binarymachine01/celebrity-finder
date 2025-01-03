import os


RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", 2))
RATE_LIMIT_PERIOD = int(os.getenv("RATE_LIMIT_PERIOD", 60))
