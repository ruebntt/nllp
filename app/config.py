import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost:5432/mydb")
RETRY_ATTEMPTS = 3
RETRY_DELAY = 2
