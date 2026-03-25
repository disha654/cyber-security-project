# Safe Lab PoC: Synthetic Event Logger with Encryption

This project is a defensive training substitute for a keylogger. It does not
capture real keyboard input, does not establish persistence, and does not send
data to any remote host other than an explicitly configured localhost test
receiver.

## What it does

- Generates synthetic keyboard events for training/demo purposes
- Encrypts event batches with `cryptography.fernet`
- Stores encrypted logs locally with UTC timestamps
- Simulates exfiltration by POSTing encrypted payloads to `127.0.0.1`
- Supports an operator kill switch via `Ctrl+C` or a stop-file trigger

## Safety constraints

- No use of `pynput` or any real keyboard hooks
- No startup persistence of any kind
- Receiver defaults to `http://127.0.0.1:8080/ingest`
- Refuses to run if the destination host is not localhost

## Files

- `main.py` - orchestration loop
- `event_generator.py` - synthetic event generation
- `crypto_logger.py` - encryption and local log persistence
- `local_receiver.py` - localhost-only test receiver
- `requirements.txt` - Python dependencies

## Setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run

Start the local receiver:

```powershell
python local_receiver.py
```

Then open:

```text
http://127.0.0.1:8080/
```

You should see a browser page titled `Local Synthetic Event Monitor`.

Run the lab PoC:

```powershell
python main.py
```

As batches arrive, they will appear on the localhost page and also be printed in
the receiver terminal.

## Kill switch

Stop the program with `Ctrl+C`, or create an empty file named `STOP` in the
project root while `main.py` is running.
