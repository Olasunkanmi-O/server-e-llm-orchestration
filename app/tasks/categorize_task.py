# app/tasks/categorize_task.py
import asyncio
from app.llm_service.db import get_pool
from app.llm_service.providers.factory import get_provider
from app.config import settings

LOW_CONFIDENCE_THRESHOLD = 0.8
provider = get_provider(settings.LLM_PROVIDER)

async def categorize_new_transactions():
    pool = await get_pool()
    async with pool.acquire() as conn:
        transactions = await conn.fetch("""
            SELECT id, description, amount
            FROM transactions
            WHERE category IS NULL
        """)
        if not transactions:
            return

        updates = []
        for tx in transactions:
            prompt = f"Categorize this transaction: '{tx['description']}' amount £{tx['amount']}"
            try:
                res = provider.generate_response(prompt)
                category = res.get("text", "Uncategorized")
                confidence = res.get("confidence", 0)
                needs_review = confidence < LOW_CONFIDENCE_THRESHOLD

                updates.append({
                    "id": tx["id"],
                    "category": category,
                    "confidence": confidence,
                    "needs_review": needs_review
                })
            except Exception as e:
                print(f"Error categorizing transaction {tx['id']}: {e}")
                continue

        for u in updates:
            await conn.execute("""
                UPDATE transactions
                SET category=$1, confidence=$2, needs_review=$3
                WHERE id=$4
            """, u["category"], u["confidence"], u["needs_review"], u["id"])

        print(f"Categorized {len(updates)} new transactions.")
