from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
import time
from urllib.parse import urlparse

import requests

from crypto_logger import CryptoLogger
from event_generator import EventGenerator


PROJECT_ROOT = Path(__file__).resolve().parent
LOG_DIR = PROJECT_ROOT / "logs"
KEY_PATH = PROJECT_ROOT / "secret.key"
STOP_FILE = PROJECT_ROOT / "STOP"
RECEIVER_URL = "http://127.0.0.1:8080/ingest"


def ensure_localhost(url: str) -> None:
    parsed = urlparse(url)
    if parsed.hostname not in {"127.0.0.1", "localhost"}:
        raise ValueError("Receiver URL must point to localhost for safe lab use.")


def send_to_receiver(receiver_url: str, encrypted_payload: bytes, log_path: Path) -> None:
    response = requests.post(
        receiver_url,
        json={
            "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "encrypted_payload_b64": encrypted_payload.decode("ascii"),
            "log_file": str(log_path.name),
            "mode": "synthetic-training",
        },
        timeout=5,
    )
    response.raise_for_status()


def main() -> None:
    ensure_localhost(RECEIVER_URL)
    logger = CryptoLogger(log_dir=LOG_DIR, key_path=KEY_PATH)
    generator = EventGenerator()

    print("Safe lab PoC running. Synthetic events only. Press Ctrl+C or create STOP to exit.")

    try:
        while True:
            if STOP_FILE.exists():
                print("Kill switch detected via STOP file. Exiting.")
                break

            batch = [asdict(generator.next_event()) for _ in range(8)]
            encrypted_payload = logger.encrypt_batch(batch)
            log_path = logger.write_encrypted_log(encrypted_payload)

            try:
                send_to_receiver(RECEIVER_URL, encrypted_payload, log_path)
                print(f"Sent encrypted synthetic batch. Local log: {log_path.name}")
            except requests.RequestException as exc:
                print(f"Receiver unavailable, batch kept locally: {exc}")

            time.sleep(2)
    except KeyboardInterrupt:
        print("Interrupted by operator. Exiting.")


if __name__ == "__main__":
    main()
