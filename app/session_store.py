from collections import defaultdict
from threading import Lock
from .models import ChatMessage


class InMemorySessionStore:
    def __init__(self, max_messages: int = 12):
        self._sessions: dict[str, list[ChatMessage]] = defaultdict(list)
        self._lock = Lock()
        self.max_messages = max_messages

    def get(self, session_id: str) -> list[ChatMessage]:
        with self._lock:
            return list(self._sessions.get(session_id, []))

    def append(self, session_id: str, message: ChatMessage) -> None:
        with self._lock:
            self._sessions[session_id].append(message)
            self._sessions[session_id] = self._sessions[session_id][-self.max_messages:]

    def clear(self, session_id: str) -> None:
        with self._lock:
            self._sessions.pop(session_id, None)
