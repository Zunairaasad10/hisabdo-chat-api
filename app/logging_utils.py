import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from .config import settings

logger = logging.getLogger("hisabdo.chat")


def configure_logging() -> None:
    path = Path(settings.log_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")


def log_chat(**data) -> None:
    record = {"timestamp": datetime.now(timezone.utc).isoformat(), **data}
    path = Path(settings.log_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    logger.info("chat_request session_id=%s status=%s", data.get("session_id"), data.get("status"))
