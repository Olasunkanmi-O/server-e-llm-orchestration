# app/llm_service/routers/review.py
from fastapi import APIRouter
from app.llm_service.db import get_pool
from app.schemas import ReviewResponse

router = APIRouter(prefix="/transactions", tags=["Review"])

@router.get("/review", response_model=ReviewResponse)
async def review_low_confidence():
    pool = await get_pool()
    async with pool.acquire() as conn:
        results = await conn.fetch("""
            SELECT id, description, amount, category, confidence
            FROM transactions
            WHERE needs_review = TRUE
        """)
        return {
            "message": f"Found {len(results)} low-confidence transactions",
            "transactions": [dict(r) for r in results]
        }
