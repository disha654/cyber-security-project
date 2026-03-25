from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import base64
import json

from cryptography.fernet import Fernet


class CryptoLogger:
    def __init__(self, log_dir: Path, key_path: Path) -> None:
        self.log_dir = log_dir
        self.key_path = key_path
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self._fernet = Fernet(self._load_or_create_key())

    def encrypt_batch(self, events: list[dict]) -> bytes:
        payload = json.dumps(events, separators=(",", ":"), sort_keys=True).encode("utf-8")
        return self._fernet.encrypt(payload)

    def write_encrypted_log(self, encrypted_payload: bytes) -> Path:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        target = self.log_dir / f"events_{timestamp}.log"
        encoded = base64.urlsafe_b64encode(encrypted_payload).decode("ascii")
        target.write_text(encoded + "\n", encoding="utf-8")
        return target

    def _load_or_create_key(self) -> bytes:
        if self.key_path.exists():
            return self.key_path.read_bytes()

        key = Fernet.generate_key()
        self.key_path.write_bytes(key)
        return key
