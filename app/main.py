# app/main.py
import asyncio
from fastapi import FastAPI
from app.routers import categorize, scenario, review, health  # import routers from the package
from app.llm_service.db import close_db_pool, get_pool  # needed for periodic tasks

app = FastAPI(
    title="AI Financial Assistant",
    description="APIs for categorizing transactions, running scenarios, and reviewing low-confidence results",
    version="1.0.0"
)

# Include routers with prefix /transactions
app.include_router(categorize.router, prefix="/transactions", tags=["Categorize"])
app.include_router(scenario.router, prefix="/transactions", tags=["Scenario"])
app.include_router(review.router, prefix="/transactions", tags=["Review"])
app.include_router(health.router, prefix="/health", tags=["Health"])  # health checks on /health

# Optional: periodic background task for categorizing new transactions
async def periodic_categorization():
    from app.routers.categorize import categorize_transactions  # import inside function to avoid startup import issues
    while True:
        pool = await get_pool()
        await categorize_transactions({"transactions": [], "user_id": None})  # dummy call for periodic processing
        await asyncio.sleep(60)  # run every 60 seconds

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(periodic_categorization())

@app.on_event("shutdown")
async def shutdown_event():
    await close_db_pool()

@app.get("/")
async def root():
    return {"message": "FiscalGuide LLM API is running!"}
