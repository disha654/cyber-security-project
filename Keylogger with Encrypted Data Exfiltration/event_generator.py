from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import random
import string


@dataclass(frozen=True)
class SyntheticEvent:
    timestamp: str
    event_type: str
    key: str
    source: str = "simulated"


class EventGenerator:
    """Produces synthetic keyboard-like events for safe lab use."""

    def __init__(self, seed: int = 1337) -> None:
        self._random = random.Random(seed)
        self._alphabet = string.ascii_letters + string.digits + " .,_-"
        self._special_keys = ["ENTER", "TAB", "SPACE", "BACKSPACE"]

    def next_event(self) -> SyntheticEvent:
        now = datetime.now(timezone.utc).isoformat()
        if self._random.random() < 0.2:
            key = self._random.choice(self._special_keys)
        else:
            key = self._random.choice(self._alphabet)

        event_type = self._random.choice(["press", "release"])
        return SyntheticEvent(timestamp=now, event_type=event_type, key=key)
