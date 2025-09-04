# app/schemas.py
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date

# Categorize
class TransactionUpdate(BaseModel):
    id: Optional[str] = None
    description: str
    amount: float
    date: Optional[date] = None
    category: str = "Uncategorized"  # default
    needs_review: bool = True

class CategorizeRequest(BaseModel):
    user_id: int
    transactions: List[TransactionUpdate]

class CategorizeResponse(BaseModel):
    status: str
    transactions: List[TransactionUpdate] = []
    low_confidence_count: int

# Scenario
class ScenarioRequest(BaseModel):
    user_id: int
    scenario_text: str  # user’s question + optional assumptions    

class ScenarioResponse(BaseModel):
    transactions: List[TransactionUpdate]

# Review
class ReviewTransaction(BaseModel):
    id: int
    category: str

class ReviewRequest(BaseModel):
    transactions: List[ReviewTransaction]

class ReviewResponse(BaseModel):
    status: str
