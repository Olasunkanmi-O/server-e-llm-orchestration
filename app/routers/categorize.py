# app/routers/categorize.py
from fastapi import APIRouter
from app.llm_service.db import get_pool
from app.llm_service.providers.factory import get_provider
from app.config import settings
from app.schemas import CategorizeRequest, CategorizeResponse
import asyncio

router = APIRouter()
provider = get_provider(settings.LLM_PROVIDER)  # e.g., OpenAIProvider
LOW_CONFIDENCE_THRESHOLD = 0.7

@router.post("/categorize", response_model=CategorizeResponse)
async def categorize_transactions(request: CategorizeRequest):
    pool = await get_pool()

    # Fetch uncategorized transactions
    async with pool.acquire() as conn:
        transactions = await conn.fetch("""
            SELECT id, description, amount
            FROM transactions
            WHERE category IS NULL
        """)

    if not transactions:
        # Return response matching your response_model
        return CategorizeResponse(
            status="no_transactions",
            transactions=[],
            low_confidence_count=0
        )

    async def categorize_single(tx):
        prompt = f"Categorize this transaction: '{tx['description']}' amount £{tx['amount']}"
        try:
            res = provider.generate_response(prompt)
            category = res.get("text", "Uncategorized")
            confidence = res.get("confidence", 0)
            needs_review = confidence < LOW_CONFIDENCE_THRESHOLD
            return {
                "id": str(tx["id"]),  # ensure ID is string if your schema expects it
                "category": category,
                "confidence": confidence,
                "needs_review": needs_review
            }
        except Exception as e:
            print(f"Error categorizing transaction {tx['id']}: {e}")
            return None

    # Run categorization concurrently
    updates = await asyncio.gather(*(categorize_single(tx) for tx in transactions))
    updates = [u for u in updates if u]  # remove failed ones

    if not updates:
        return CategorizeResponse(
            status="no_transactions_categorized",
            transactions=[],
            low_confidence_count=0
        )

    # Bulk update in DB asynchronously
    async with pool.acquire() as conn:
        async with conn.transaction():
            await asyncio.gather(*[
                conn.execute("""
                    UPDATE transactions
                    SET category=$1, confidence=$2, needs_verification=$3
                    WHERE id=$4
                """, u["category"], u["confidence"], u["needs_review"], u["id"])
                for u in updates
            ])

    return CategorizeResponse(
        status="success",
        transactions=updates,
        low_confidence_count=sum(1 for u in updates if u["needs_review"])
    )
