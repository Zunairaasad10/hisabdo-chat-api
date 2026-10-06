# HisabDo AI Chat API

Functional FastAPI prototype for the HisabDo business assistant.

## Structure

```text
app/
  main.py              # FastAPI routes
  models.py            # Pydantic request/response schemas
  prompts.py           # Versioned HisabDo system prompt
  llm.py               # OpenAI Responses API adapter
  session_store.py     # Basic in-memory conversation memory
  logging_utils.py     # JSONL request/response logging
  config.py            # Environment configuration

tests/
  test_api.py
  evaluation_cases.json

evaluate.py            # Live business-query evaluation runner
```

## Run locally

```bash
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env
# Put the real OPENAI_API_KEY in .env
uvicorn app.main:app --reload
```

API docs: `http://127.0.0.1:8000/docs`

## Chat request

```json
{
  "session_id": "business-001",
  "message": "My sales are 100000 and expenses are 65000. What is my profit?"
}
```

POST `/api/v1/chat`

## Chat response

```json
{
  "session_id": "business-001",
  "message": "Your profit is 35,000 ...",
  "model": "gpt-6-luna",
  "timestamp": "2026-10-06T00:00:00Z"
}
```

## Testing

Run API tests without an LLM key:

```bash
pytest -q
```

Run live evaluation after configuring the API key:

```bash
python evaluate.py
```

The evaluation runner writes `logs/evaluation.jsonl`. Each case contains the query, expected behavior, live answer, and a manual-review field. This makes the initial evaluation log auditable instead of pretending that keyword matching proves answer accuracy.

## Production note

The current session store is intentionally in-memory for the first prototype. For deployment, replace it with Redis/PostgreSQL and add authentication, rate limiting, request IDs, structured observability, and secrets management.
