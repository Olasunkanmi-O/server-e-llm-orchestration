# llm_service/pipeline/transaction_pipeline.py

from app.db import get_pool
from app.providers.factory import get_provider

CONFIDENCE_THRESHOLD = 0.8  # Transactions below this require user review

async def process_new_transactions(user_id: int):
    provider = get_provider()
    pool = await get_pool()
    
    async with pool.acquire() as conn:
        # Fetch uncategorized transactions
        transactions = await conn.fetch("""
            SELECT id, description, amount
            FROM transactions
            WHERE user_id = $1 AND category IS NULL
        """, user_id)

        if not transactions:
            return {"message": "No new transactions to process."}

        for tx in transactions:
            prompt = f"Categorize this transaction: '{tx['description']}' Amount: £{tx['amount']}. Respond with category and confidence score."

            try:
                res = provider.generate_response(prompt)
                category = res.get("category", "Uncategorized")
                confidence = res.get("confidence", 1.0)  # Default 1.0 if provider doesn't return it

                needs_review = confidence < CONFIDENCE_THRESHOLD

                await conn.execute("""
                    UPDATE transactions
                    SET category=$1, confidence=$2, needs_review=$3
                    WHERE id=$4
                """, category, confidence, needs_review, tx["id"])

            except Exception as e:
                print(f"Failed to categorize transaction {tx['id']}: {str(e)}")

    return {"message": f"{len(transactions)} transactions processed."}
