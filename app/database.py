from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from loguru import logger
from config import DATABASE_URL, RETRY_ATTEMPTS, RETRY_DELAY
import asyncio

engine = None
async_session = None

async def init_db():
    global engine, async_session
    for attempt in range(RETRY_ATTEMPTS):
        try:
            engine = create_async_engine(DATABASE_URL, echo=False, pool_size=10, max_overflow=20)
            async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
            # Проверкa соединения
            async with engine.begin() as conn:
                await conn.execute("SELECT 1")
            logger.info("Database connection established")
            break
        except Exception as e:
            logger.error(f"Database connection failed (attempt {attempt + 1}): {e}")
            if attempt < RETRY_ATTEMPTS - 1:
                await asyncio.sleep(RETRY_DELAY)
            else:
                raise

async def get_session():
    if async_session is None:
        await init_db()
    return async_session()
