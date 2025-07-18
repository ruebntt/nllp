import pytest
from sqlalchemy import select
from app.database import get_db
from app.models import Item

@pytest.mark.asyncio
async def test_create_item():
    async with get_db() as db:
        new_item = Item(value=42)
        db.add(new_item)
        await db.commit()
        result = await db.execute(select(Item).where(Item.value == 42))
        item = result.scalar_one()
        assert item.value == 42
