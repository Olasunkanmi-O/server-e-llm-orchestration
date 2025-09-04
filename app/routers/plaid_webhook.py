# app/llm_service/routers/plaid_webhook.py
from fastapi import APIRouter, Request, HTTPException
from ..pipeline.transaction_pipeline import process_new_transactions
from ..config import settings
from plaid import Client

router = APIRouter()

# Initialize Plaid client
plaid_client = Client(
    client_id=settings.PLAID_CLIENT_ID,
    secret=settings.PLAID_SECRET,
    environment=settings.PLAID_ENV  # "sandbox", "development", "production"
)

@router.post("/plaid/webhook")
async def plaid_webhook(request: Request):
    """
    Receive Plaid webhook, fetch new transactions, process via pipeline
    """
    try:
        data = await request.json()
        item_id = data.get("item_id")
        webhook_type = data.get("webhook_type")
        webhook_code = data.get("webhook_code")

        # For demonstration, only process new transactions
        if webhook_type == "TRANSACTIONS" and webhook_code in ["INITIAL_UPDATE", "HISTORICAL_UPDATE", "DEFAULT_UPDATE", "TRANSACTIONS:ADDED"]:
            # Lookup user_id for this item_id
            pool = await get_pool()
            async with pool.acquire() as conn:
                row = await conn.fetchrow(
                    "SELECT user_id, access_token FROM user_plaid_accounts WHERE item_id=$1",
                    item_id
                )
                if not row:
                    raise HTTPException(status_code=404, detail="Plaid item not linked to user")

                user_id = row["user_id"]
                access_token = row["access_token"]

            # Fetch new transactions from Plaid
            response = plaid_client.Transactions.get(access_token, start_date="2025-01-01", end_date="2025-12-31")
            new_transactions = [
                {
                    "description": tx["name"],
                    "amount": tx["amount"],
                    "date": tx["date"]
                }
                for tx in response["transactions"]
            ]

            # Process transactions via pipeline
            categorized = await process_new_transactions(user_id, new_transactions)
            return {"status": "success", "transactions_processed": len(categorized)}

        return {"status": "ignored"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
