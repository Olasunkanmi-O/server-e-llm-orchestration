# app/routers/scenario.py
from fastapi import APIRouter, HTTPException
from app.llm_service.db import get_pool
from app.llm_service.providers.factory import get_provider
from app.config import settings
from app.schemas import ScenarioRequest, ScenarioResponse

router = APIRouter()
provider = get_provider(settings.LLM_PROVIDER)

@router.post("/scenario", response_model=ScenarioResponse)
async def run_scenario(request: ScenarioRequest):
    if not request.user_id or not request.scenario_request:
        raise HTTPException(status_code=400, detail="user_id and scenario_request are required")

    pool = await get_pool()

    # Fetch all transactions for this user
    async with pool.acquire() as conn:
        transactions = await conn.fetch("""
            SELECT date, description, amount, category, needs_verification
            FROM transactions
            WHERE user_id = $1
        """, request.user_id)

    # Convert transactions to a list of dicts for the LLM
    transaction_list = [
        {
            "date": str(tx["date"]),
            "description": tx["description"],
            "amount": float(tx["amount"]),
            "category": tx["category"],
            "needs_verification": tx["needs_verification"]
        }
        for tx in transactions
    ]

    # Build the prompt dynamically
    prompt = f"""
You are an AI financial assistant. Only use the following transactions
to answer the user's question. Do not access any other data.
Transactions: {transaction_list}

User question: {request.scenario_request}
"""

    try:
        response = provider.generate_response(prompt)
        answer = response.get("text", "Sorry, I could not find an answer based on your transactions.")
        confidence = response.get("confidence", 0)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM error: {e}")

    return ScenarioResponse(
        answer=answer,
        confidence=confidence
    )
