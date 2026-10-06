import json
from pathlib import Path

from app.llm import GroqChatService


CASES = json.loads(
    Path("tests/evaluation_cases.json").read_text(encoding="utf-8")
)

service = GroqChatService()

if service.client is None:
    raise SystemExit("Set GROQ_API_KEY before running the live evaluation.")

out = Path("logs/evaluation.jsonl")

with out.open("a", encoding="utf-8") as f:
    for case in CASES:
        answer = service.generate([], case["query"])

        record = {
            "id": case["id"],
            "query": case["query"],
            "expected_behavior": case["expected_behavior"],
            "answer": answer,
            "review": "PENDING_MANUAL_REVIEW"
        }

        f.write(
            json.dumps(record, ensure_ascii=False) + "\n"
        )

        print(f"[{case['id']}] {answer}\n")