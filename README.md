## Flow Explanation

User Signup & Bank Connection

Frontend calls backend → user signs up and connects bank via Plaid.

Plaid returns access_token & item_id → stored in Postgres.

Initial Transaction Fetch

Backend fetches all historical transactions from Plaid → inserted into transactions table.

Transaction Pipeline (LLM) categorizes each transaction and stores category + confidence.

Low-confidence txns are flagged for user verification.

New Transactions

Plaid triggers webhook for new transactions → backend fetches only new txns → pipeline categorizes them.

Dashboard Display

Frontend shows categorized transactions:

High-confidence → auto-approved

Low-confidence → dropdown for user to verify

Scenario Analysis

User submits a “what-if” scenario.

Backend fetches all categorized transactions.

Prompt sent to LLM → analysis returned → displayed on dashboard.

Pluggable LLM

provider can be OpenAI, DeepSeek, or other.

Easy to swap providers without changing backend logic.

## folder structure

fiscalguide-llm/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
|   |__ schemas
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── categorize.py
│   │   ├── scenario.py
│   │   └── health.py
│   │
│   |── llm_service/
│   |   ├── __init__.py
│   |   ├── providers/
│   |   │   ├── __init__.py
│   |   │   ├── factory.py
│   |   │   ├── openai_provider.py
│   |   │   ├── anthropic_provider.py
│   |   │   └── deepseek_provider.py
|   |   |___Pipeline/
|   |   |   |__transaction_pipeline
|   |   |   |
|   |   |
|   |   |
|   |   |___db
|   |   |
|   |
|   |__ Tasks/
|
├── .env
├── requirements.txt
└── README.md
