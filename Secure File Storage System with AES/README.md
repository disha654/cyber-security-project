# Secure File Storage System with AES

Local file encryption and decryption utility built with Python and AES-256-GCM.

## Security features

- AES-256-GCM encryption for file contents
- Per-file random data encryption key
- Password-based key derivation with `scrypt`
- Encrypted metadata storage for file name, timestamp, hash, and size
- SHA-256 verification after decryption to detect tampering

## Setup

```bash
pip install -r requirements.txt
```

## Usage

Encrypt a file:

```bash
python secure_storage.py encrypt path/to/file.txt
```

Decrypt a file:

```bash
python secure_storage.py decrypt path/to/file.txt.enc
```

List recorded encrypted files:

```bash
python secure_storage.py list
```

Decrypt and show protected metadata:

```bash
python secure_storage.py list --details
```

Launch the graphical user interface (Tkinter):

```bash
python secure_storage.py gui
```

Launch the modern Web UI (Flask):

```bash
python secure_storage.py serve
```

The tool writes encrypted files with the `.enc` extension.
 `.secure_storage/manifest.json` stores only non-sensitive tracking data, while file metadata remains encrypted inside each container.
