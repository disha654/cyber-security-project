import argparse
import base64
import getpass
import hashlib
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


APP_DIR_NAME = ".secure_storage"
MANIFEST_FILE_NAME = "manifest.json"
KDF_SALT_SIZE = 16
AES_KEY_SIZE = 32
GCM_NONCE_SIZE = 12
SCRYPT_N = 2**14
SCRYPT_R = 8
SCRYPT_P = 1


class SecureStorageError(Exception):
    pass


def b64encode(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def b64decode(data: str) -> bytes:
    return base64.b64decode(data.encode("ascii"))


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def derive_key(password: str, salt: bytes) -> bytes:
    kdf = Scrypt(
        salt=salt,
        length=AES_KEY_SIZE,
        n=SCRYPT_N,
        r=SCRYPT_R,
        p=SCRYPT_P,
    )
    return kdf.derive(password.encode("utf-8"))


def aesgcm_encrypt(key: bytes, plaintext: bytes, aad: bytes) -> Dict[str, str]:
    nonce = os.urandom(GCM_NONCE_SIZE)
    ciphertext = AESGCM(key).encrypt(nonce, plaintext, aad)
    return {
        "nonce": b64encode(nonce),
        "ciphertext": b64encode(ciphertext),
    }


def aesgcm_decrypt(key: bytes, payload: Dict[str, str], aad: bytes) -> bytes:
    nonce = b64decode(payload["nonce"])
    ciphertext = b64decode(payload["ciphertext"])
    try:
        return AESGCM(key).decrypt(nonce, ciphertext, aad)
    except InvalidTag as exc:
        raise SecureStorageError(
            "Decryption failed. The password is incorrect or the encrypted file was tampered with."
        ) from exc


@dataclass
class StoragePaths:
    app_dir: Path
    manifest_file: Path


class SecureFileStorage:
    def __init__(self, base_dir: Optional[Path] = None) -> None:
        root = base_dir or Path.cwd()
        app_dir = root / APP_DIR_NAME
        self.paths = StoragePaths(
            app_dir=app_dir,
            manifest_file=app_dir / MANIFEST_FILE_NAME,
        )
        self.paths.app_dir.mkdir(parents=True, exist_ok=True)

    def load_manifest(self) -> Dict[str, Any]:
        if not self.paths.manifest_file.exists():
            return {"files": []}

        with self.paths.manifest_file.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
            data.setdefault("files", [])
            return data

    def save_manifest(self, manifest: Dict[str, Any]) -> None:
        with self.paths.manifest_file.open("w", encoding="utf-8") as handle:
            json.dump(manifest, handle, indent=2)

    def encrypt_file(self, source_path: Path, password: str, output_path: Optional[Path] = None) -> Path:
        if not source_path.exists() or not source_path.is_file():
            raise SecureStorageError(f"Input file not found: {source_path}")

        plaintext = source_path.read_bytes()
        plaintext_hash = hashlib.sha256(plaintext).hexdigest()
        file_key = os.urandom(AES_KEY_SIZE)
        salt = os.urandom(KDF_SALT_SIZE)
        key_encryption_key = derive_key(password, salt)

        metadata = {
            "original_name": source_path.name,
            "encrypted_at": utc_now(),
            "sha256": plaintext_hash,
            "size_bytes": len(plaintext),
        }

        encrypted_metadata = aesgcm_encrypt(
            file_key,
            json.dumps(metadata).encode("utf-8"),
            aad=b"metadata:v1",
        )
        encrypted_payload = aesgcm_encrypt(
            file_key,
            plaintext,
            aad=b"payload:v1",
        )
        wrapped_file_key = aesgcm_encrypt(
            key_encryption_key,
            file_key,
            aad=b"file-key:v1",
        )

        envelope = {
            "version": 1,
            "algorithms": {
                "payload": "AES-256-GCM",
                "key_wrap": "AES-256-GCM",
                "kdf": "scrypt",
                "hash": "SHA-256",
            },
            "kdf": {
                "salt": b64encode(salt),
                "n": SCRYPT_N,
                "r": SCRYPT_R,
                "p": SCRYPT_P,
            },
            "wrapped_file_key": wrapped_file_key,
            "metadata": encrypted_metadata,
            "payload": encrypted_payload,
        }

        destination = output_path or source_path.with_suffix(source_path.suffix + ".enc")
        with destination.open("w", encoding="utf-8") as handle:
            json.dump(envelope, handle, indent=2)

        self._update_manifest(destination, metadata)
        return destination

    def decrypt_file(self, encrypted_path: Path, password: str, output_dir: Optional[Path] = None) -> Path:
        if not encrypted_path.exists() or not encrypted_path.is_file():
            raise SecureStorageError(f"Encrypted file not found: {encrypted_path}")

        with encrypted_path.open("r", encoding="utf-8") as handle:
            envelope = json.load(handle)

        salt = b64decode(envelope["kdf"]["salt"])
        key_encryption_key = derive_key(password, salt)
        file_key = aesgcm_decrypt(
            key_encryption_key,
            envelope["wrapped_file_key"],
            aad=b"file-key:v1",
        )

        metadata_bytes = aesgcm_decrypt(file_key, envelope["metadata"], aad=b"metadata:v1")
        metadata = json.loads(metadata_bytes.decode("utf-8"))
        plaintext = aesgcm_decrypt(file_key, envelope["payload"], aad=b"payload:v1")

        computed_hash = hashlib.sha256(plaintext).hexdigest()
        if computed_hash != metadata["sha256"]:
            raise SecureStorageError(
                "Hash verification failed. The decrypted file does not match the stored integrity record."
            )

        destination_dir = output_dir or encrypted_path.parent
        destination_dir.mkdir(parents=True, exist_ok=True)
        destination = destination_dir / metadata["original_name"]
        destination.write_bytes(plaintext)
        return destination

    def read_metadata(self, encrypted_path: Path, password: str) -> Dict[str, Any]:
        if not encrypted_path.exists() or not encrypted_path.is_file():
            raise SecureStorageError(f"Encrypted file not found: {encrypted_path}")

        with encrypted_path.open("r", encoding="utf-8") as handle:
            envelope = json.load(handle)

        salt = b64decode(envelope["kdf"]["salt"])
        key_encryption_key = derive_key(password, salt)
        file_key = aesgcm_decrypt(
            key_encryption_key,
            envelope["wrapped_file_key"],
            aad=b"file-key:v1",
        )
        metadata_bytes = aesgcm_decrypt(file_key, envelope["metadata"], aad=b"metadata:v1")
        return json.loads(metadata_bytes.decode("utf-8"))

    def list_files(self) -> Dict[str, Any]:
        return self.load_manifest()

    def _update_manifest(self, encrypted_path: Path, metadata: Dict[str, Any]) -> None:
        manifest = self.load_manifest()
        files = [entry for entry in manifest["files"] if entry["encrypted_path"] != str(encrypted_path)]
        files.append(
            {
                "encrypted_path": str(encrypted_path),
                "recorded_at": utc_now(),
                "container_sha256": sha256_file(encrypted_path),
                "original_extension": Path(metadata["original_name"]).suffix,
            }
        )
        manifest["files"] = sorted(files, key=lambda entry: entry["recorded_at"], reverse=True)
        self.save_manifest(manifest)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Secure local file storage with AES-256-GCM encryption.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    encrypt_parser = subparsers.add_parser("encrypt", help="Encrypt a file into a .enc container.")
    encrypt_parser.add_argument("input", type=Path, help="Path to the file to encrypt.")
    encrypt_parser.add_argument("-o", "--output", type=Path, help="Optional output .enc path.")

    decrypt_parser = subparsers.add_parser("decrypt", help="Decrypt a previously encrypted .enc file.")
    decrypt_parser.add_argument("input", type=Path, help="Path to the encrypted .enc file.")
    decrypt_parser.add_argument("-o", "--output-dir", type=Path, help="Optional output directory.")

    list_parser = subparsers.add_parser("list", help="List stored encrypted files.")
    list_parser.add_argument(
        "--details",
        action="store_true",
        help="Decrypt and display protected metadata for each file. Requires the password.",
    )

    subparsers.add_parser("gui", help="Launch the graphical user interface (Tkinter).")
    subparsers.add_parser("serve", help="Launch the web-based graphical interface (Flask).")
    return parser


def launch_gui() -> None:
    import tkinter as tk
    from tkinter import filedialog, messagebox, simpledialog

    storage = SecureFileStorage()
    root = tk.Tk()
    root.title("AES-256 Secure File Storage")
    root.geometry("600x400")

    def handle_encrypt():
        source_path = filedialog.askopenfilename(title="Select File to Encrypt")
        if not source_path:
            return
        
        password = simpledialog.askstring("Password", "Enter encryption password:", show="*")
        if not password:
            return
        
        confirm = simpledialog.askstring("Password", "Confirm encryption password:", show="*")
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        try:
            destination = storage.encrypt_file(Path(source_path), password)
            messagebox.showinfo("Success", f"File encrypted and saved to:\n{destination}")
            refresh_list()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def handle_decrypt():
        encrypted_path = filedialog.askopenfilename(
            title="Select Encrypted File (.enc)",
            filetypes=[("Encrypted files", "*.enc"), ("All files", "*.*")]
        )
        if not encrypted_path:
            return
        
        password = simpledialog.askstring("Password", "Enter decryption password:", show="*")
        if not password:
            return
        
        output_dir = filedialog.askdirectory(title="Select Output Directory for Restored File")
        if not output_dir:
            return

        try:
            destination = storage.decrypt_file(Path(encrypted_path), password, Path(output_dir))
            messagebox.showinfo("Success", f"File decrypted and restored to:\n{destination}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refresh_list():
        listbox.delete(0, tk.END)
        manifest = storage.list_files()
        for entry in manifest["files"]:
            listbox.insert(tk.END, f"{entry['encrypted_path']} (Recorded: {entry['recorded_at']})")

    # Layout
    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack(fill=tk.BOTH, expand=True)

    btn_frame = tk.Frame(frame)
    btn_frame.pack(fill=tk.X, pady=5)

    tk.Button(btn_frame, text="Encrypt File", command=handle_encrypt, width=20).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Decrypt File", command=handle_decrypt, width=20).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Refresh List", command=refresh_list, width=20).pack(side=tk.LEFT, padx=5)

    tk.Label(frame, text="Encrypted Files History:").pack(anchor=tk.W, pady=(10, 0))
    
    listbox = tk.Listbox(frame, width=80, height=15)
    listbox.pack(fill=tk.BOTH, expand=True, pady=5)
    
    refresh_list()
    root.mainloop()


def prompt_password(confirm: bool = False) -> str:
    password = getpass.getpass("Enter password: ")
    if not password:
        raise SecureStorageError("Password cannot be empty.")

    if confirm:
        confirmation = getpass.getpass("Confirm password: ")
        if password != confirmation:
            raise SecureStorageError("Passwords do not match.")

    return password


def run_cli() -> int:
    parser = build_parser()
    args = parser.parse_args()
    storage = SecureFileStorage()

    try:
        if args.command == "encrypt":
            password = prompt_password(confirm=True)
            destination = storage.encrypt_file(args.input, password, args.output)
            print(f"Encrypted file saved to: {destination}")
            print(f"Source SHA-256: {sha256_file(args.input)}")
            return 0

        if args.command == "decrypt":
            password = prompt_password(confirm=False)
            destination = storage.decrypt_file(args.input, password, args.output_dir)
            print(f"Decrypted file restored to: {destination}")
            print(f"Restored SHA-256: {sha256_file(destination)}")
            return 0

        if args.command == "list":
            manifest = storage.list_files()
            if not manifest["files"]:
                print("No encrypted files recorded yet.")
                return 0

            password = prompt_password(confirm=False) if args.details else None
            for entry in manifest["files"]:
                summary = (
                    f"{entry['encrypted_path']} | recorded_at={entry['recorded_at']} | "
                    f"container_sha256={entry['container_sha256']}"
                )
                if password:
                    try:
                        metadata = storage.read_metadata(Path(entry["encrypted_path"]), password)
                        summary += (
                            f" | original={metadata['original_name']} | "
                            f"encrypted_at={metadata['encrypted_at']} | sha256={metadata['sha256']}"
                        )
                    except SecureStorageError:
                        summary += " | [Failed to decrypt metadata]"
                print(summary)
            return 0

        if args.command == "gui":
            launch_gui()
            return 0

        if args.command == "serve":
            from app import app
            print("Launching Web UI on http://127.0.0.1:5000")
            app.run(host="127.0.0.1", port=5000)
            return 0

    except SecureStorageError as exc:
        print(f"Error: {exc}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(run_cli())
