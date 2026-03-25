import os
import io
import shutil
from pathlib import Path
from flask import Flask, request, jsonify, send_file, render_template_string
from secure_storage import SecureFileStorage, SecureStorageError

app = Flask(__name__)
storage = SecureFileStorage()

# HTML Template with Tailwind CSS for a modern, colorful look
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AES Secure Storage</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .glass { background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); border-radius: 1rem; box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37); }
    </style>
</head>
<body class="p-4 md:p-8 font-sans">
    <div class="max-w-4xl mx-auto">
        <!-- Header -->
        <div class="text-center mb-8 text-white">
            <h1 class="text-4xl font-extrabold mb-2"><i class="fas fa-shield-alt mr-2"></i>Secure AES Storage</h1>
            <p class="text-indigo-100">Localhost AES-256-GCM File Encryption System</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <!-- Encryption Section -->
            <div class="glass p-6">
                <h2 class="text-2xl font-bold mb-4 text-indigo-700 flex items-center">
                    <i class="fas fa-lock mr-2"></i> Encrypt File
                </h2>
                <div class="space-y-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Choose File</label>
                        <input type="file" id="encryptFile" class="mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Encryption Password</label>
                        <input type="password" id="encryptPass" placeholder="••••••••" class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md text-sm shadow-sm placeholder-gray-400 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500">
                    </div>
                    <button onclick="handleEncrypt()" class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded transition duration-200">
                        Securely Encrypt
                    </button>
                    <div id="encryptStatus" class="text-sm mt-2 hidden"></div>
                </div>
            </div>

            <!-- Decryption Section -->
            <div class="glass p-6">
                <h2 class="text-2xl font-bold mb-4 text-purple-700 flex items-center">
                    <i class="fas fa-unlock-alt mr-2"></i> Decrypt File
                </h2>
                <div class="space-y-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Choose .enc File</label>
                        <input type="file" id="decryptFile" accept=".enc" class="mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-purple-50 file:text-purple-700 hover:file:bg-purple-100">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Decryption Password</label>
                        <input type="password" id="decryptPass" placeholder="••••••••" class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md text-sm shadow-sm placeholder-gray-400 focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500">
                    </div>
                    <button onclick="handleDecrypt()" class="w-full bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded transition duration-200">
                        Restore Original
                    </button>
                    <div id="decryptStatus" class="text-sm mt-2 hidden"></div>
                </div>
            </div>
        </div>

        <!-- History / Manifest Section -->
        <div class="glass mt-8 p-6">
            <h2 class="text-2xl font-bold mb-4 text-gray-800 flex items-center">
                <i class="fas fa-history mr-2 text-gray-500"></i> Encrypted Files History
                <button onclick="loadManifest()" class="ml-auto text-sm text-indigo-600 hover:underline"><i class="fas fa-sync-alt"></i> Refresh</button>
            </h2>
            <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200">
                    <thead>
                        <tr class="text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">
                            <th class="px-4 py-2">Path</th>
                            <th class="px-4 py-2">Date Recorded</th>
                            <th class="px-4 py-2">Type</th>
                        </tr>
                    </thead>
                    <tbody id="manifestList" class="divide-y divide-gray-100 text-sm text-gray-700">
                        <!-- Loaded dynamically -->
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        async function loadManifest() {
            const resp = await fetch('/api/files');
            const data = await resp.json();
            const list = document.getElementById('manifestList');
            list.innerHTML = '';
            data.files.forEach(f => {
                const row = `<tr>
                    <td class="px-4 py-2 font-mono text-xs truncate max-w-xs" title="${f.encrypted_path}">${f.encrypted_path}</td>
                    <td class="px-4 py-2">${new Date(f.recorded_at).toLocaleString()}</td>
                    <td class="px-4 py-2"><span class="px-2 py-1 bg-gray-200 rounded text-xs">${f.original_extension || '???'}</span></td>
                </tr>`;
                list.insertAdjacentHTML('beforeend', row);
            });
        }

        async function handleEncrypt() {
            const fileInput = document.getElementById('encryptFile');
            const password = document.getElementById('encryptPass').value;
            const status = document.getElementById('encryptStatus');

            if (!fileInput.files[0] || !password) {
                showStatus(status, "File and password required", false);
                return;
            }

            const formData = new FormData();
            formData.append('file', fileInput.files[0]);
            formData.append('password', password);

            showStatus(status, "Encrypting...", true);
            try {
                const resp = await fetch('/api/encrypt', { method: 'POST', body: formData });
                const data = await resp.json();
                if (resp.ok) {
                    showStatus(status, `Success! Saved as ${data.filename}`, true);
                    loadManifest();
                } else {
                    showStatus(status, data.error, false);
                }
            } catch (e) {
                showStatus(status, "Error connecting to server", false);
            }
        }

        async function handleDecrypt() {
            const fileInput = document.getElementById('decryptFile');
            const password = document.getElementById('decryptPass').value;
            const status = document.getElementById('decryptStatus');

            if (!fileInput.files[0] || !password) {
                showStatus(status, "File and password required", false);
                return;
            }

            const formData = new FormData();
            formData.append('file', fileInput.files[0]);
            formData.append('password', password);

            showStatus(status, "Decrypting and Restoring...", true);
            try {
                const resp = await fetch('/api/decrypt', { method: 'POST', body: formData });
                if (resp.ok) {
                    const blob = await resp.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    // Get filename from header if possible, or fallback
                    const cd = resp.headers.get('Content-Disposition');
                    const filename = cd ? cd.split('filename=')[1].replace(/"/g, '') : 'restored_file';
                    a.download = filename;
                    document.body.appendChild(a);
                    a.click();
                    a.remove();
                    showStatus(status, "Decryption successful! File downloaded.", true);
                } else {
                    const data = await resp.json();
                    showStatus(status, data.error, false);
                }
            } catch (e) {
                showStatus(status, "Error connecting to server", false);
            }
        }

        function showStatus(elem, msg, isSuccess) {
            elem.innerText = msg;
            elem.className = `text-sm mt-2 block ${isSuccess ? 'text-green-600' : 'text-red-600'}`;
        }

        loadManifest();
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/files")
def list_files():
    return jsonify(storage.list_files())

@app.route("/api/encrypt", methods=["POST"])
def encrypt():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    password = request.form.get('password')
    
    if not password:
        return jsonify({"error": "No password provided"}), 400

    # Save temp file
    temp_dir = Path("temp_uploads")
    temp_dir.mkdir(exist_ok=True)
    source_path = temp_dir / file.filename
    file.save(source_path)

    try:
        dest_path = storage.encrypt_file(source_path, password)
        return jsonify({
            "success": True, 
            "filename": dest_path.name,
            "path": str(dest_path)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if source_path.exists():
            source_path.unlink()

@app.route("/api/decrypt", methods=["POST"])
def decrypt():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    password = request.form.get('password')
    
    if not password:
        return jsonify({"error": "No password provided"}), 400

    temp_dir = Path("temp_decrypt")
    temp_dir.mkdir(exist_ok=True)
    encrypted_path = temp_dir / file.filename
    file.save(encrypted_path)

    try:
        # Decrypt to a temporary restored location
        restored_dir = Path("temp_restored")
        restored_path = storage.decrypt_file(encrypted_path, password, restored_dir)
        
        # Send file back to user
        return send_file(
            restored_path,
            as_attachment=True,
            download_name=restored_path.name
        )
    except SecureStorageError as e:
        return jsonify({"error": str(e)}), 403
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Cleanup temp encrypted file
        if encrypted_path.exists():
            encrypted_path.unlink()
        # Cleanup restored file will be handled later or on next request to keep it simple
        # (In a production app, we'd use a more robust cleanup or serve from memory)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
