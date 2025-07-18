from fastapi import FastAPI, HTTPException, Depends
from loguru import logger
from insertion_sort import insertion_sort
from database import init_db, get_session
from models import User
from pydantic import BaseModel

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await init_db()

class SortRequest(BaseModel):
    array: list[int]

@app.post("/sort/")
async def sort_array(data: SortRequest):
    try:
        sorted_array = insertion_sort(data.array.copy())
        return {"sorted": sorted_array}
    except Exception as e:
        logger.error(f"Error during sorting: {e}")
        raise HTTPException(status_code=500, detail="Sorting failed")
