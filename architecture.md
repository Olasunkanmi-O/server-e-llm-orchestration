+-------------------+
|   Frontend (React/Vite)   |
|-------------------|
| - Signup / Login          |
| - Connect Bank (Plaid)    |
| - Dashboard               |
| - Scenario Input Form     |
+-----------+---------------+
            |
            v
+-------------------+
| Backend (FastAPI) |
|-------------------|
| - Authentication  |
| - /categorize     |<---------------------------------------+
| - /run_scenario   |                                        |
| - /plaid/webhook  |                                        |
+-----------+-------+                                        |
            |                                                |
            v                                                |
+-------------------+                                       |
|  PostgreSQL       |                                       |
|-------------------|                                       |
| Tables:            |                                       |
| - users            |                                       |
| - user_plaid_accounts |                                    |
| - transactions     |                                       |
+-----------+-------+                                       |
            |                                                |
            v                                                |
+-------------------------------+                             |
| Transaction Pipeline / LLM    |                             |
|-------------------------------|                             |
| - Fetch uncategorized txns    |                             |
| - Call LLM for categorization |                             |
| - Assign category & confidence|                             |
| - Flag low-confidence txns    |                             |
+-----------+-------------------+                             |
            |                                                |
            v                                                |
+-------------------------------+                             |
| Scenario Analysis Service (LLM)|                             |
|-------------------------------|                             |
| - Fetch categorized txns       |                             |
| - Format prompt for scenario   |                             |
| - Call LLM provider (OpenAI/DeepSeek)                      |
| - Return recommendation        |                             |
+-------------------------------+                             |
                                                               |
                +-----------------------------------------------+
                |
+-------------------------------+
| Plaid (Open Banking)          |
|-------------------------------|
| - Initial transaction fetch   |
| - Webhooks for new txns       |
+-------------------------------+
