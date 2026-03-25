from __future__ import annotations

from collections import deque
from html import escape
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse


HOST = "127.0.0.1"
PORT = 8080
MAX_PAYLOADS = 20
RECENT_PAYLOADS: deque[dict] = deque(maxlen=MAX_PAYLOADS)


HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Local Synthetic Event Monitor</title>
  <style>
    :root {
      color-scheme: light;
      --bg: #f3efe7;
      --panel: #fffaf2;
      --ink: #1f2937;
      --muted: #6b7280;
      --line: #d6cfc2;
      --accent: #0f766e;
      --accent-soft: #dff5f2;
      --danger: #7c2d12;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: Georgia, "Times New Roman", serif;
      background:
        radial-gradient(circle at top left, #fdf8ef 0, #f3efe7 48%, #ebe4d8 100%);
      color: var(--ink);
    }
    .wrap {
      max-width: 980px;
      margin: 0 auto;
      padding: 32px 20px 48px;
    }
    .hero, .panel {
      background: rgba(255, 250, 242, 0.92);
      border: 1px solid var(--line);
      border-radius: 18px;
      box-shadow: 0 10px 30px rgba(31, 41, 55, 0.08);
    }
    .hero {
      padding: 24px;
      margin-bottom: 20px;
    }
    h1 {
      margin: 0 0 10px;
      font-size: clamp(2rem, 4vw, 3.2rem);
      line-height: 1;
    }
    p {
      margin: 0;
      color: var(--muted);
      font-size: 1rem;
      line-height: 1.6;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 16px;
      margin: 20px 0;
    }
    .panel {
      padding: 18px;
    }
    .label {
      display: inline-block;
      padding: 6px 10px;
      border-radius: 999px;
      background: var(--accent-soft);
      color: var(--accent);
      font-size: 0.85rem;
      margin-bottom: 12px;
    }
    .value {
      font-size: 1.4rem;
      margin: 0;
    }
    .subtle {
      margin-top: 8px;
      color: var(--muted);
      font-size: 0.95rem;
    }
    .payloads {
      display: grid;
      gap: 14px;
      margin-top: 18px;
    }
    .payload {
      border: 1px solid var(--line);
      border-radius: 14px;
      padding: 14px;
      background: #fff;
    }
    .payload h3 {
      margin: 0 0 8px;
      font-size: 1rem;
    }
    pre {
      margin: 0;
      white-space: pre-wrap;
      word-break: break-word;
      font-family: Consolas, "Courier New", monospace;
      font-size: 0.9rem;
      background: #fcfaf6;
      border-radius: 10px;
      padding: 12px;
      border: 1px solid #ece4d7;
    }
    .empty {
      color: var(--danger);
      font-style: italic;
    }
  </style>
</head>
<body>
  <main class="wrap">
    <section class="hero">
      <h1>Local Synthetic Event Monitor</h1>
      <p>
        This localhost page shows payloads received from the safe training demo.
        Keep this page open, then run <code>python main.py</code> in another terminal.
      </p>
    </section>

    <section class="grid">
      <article class="panel">
        <span class="label">Status</span>
        <p class="value">Receiver running</p>
        <p class="subtle">Listening on http://127.0.0.1:8080/</p>
      </article>
      <article class="panel">
        <span class="label">Endpoint</span>
        <p class="value">POST /ingest</p>
        <p class="subtle">Browser visits are safe now. Incoming demo data appears below.</p>
      </article>
    </section>

    <section class="panel">
      <span class="label">Recent Payloads</span>
      <div id="payloads" class="payloads">
        <p class="empty">No payloads received yet.</p>
      </div>
    </section>
  </main>

  <script>
    async function refreshPayloads() {
      const container = document.getElementById("payloads");
      try {
        const response = await fetch("/api/payloads", { cache: "no-store" });
        const payloads = await response.json();
        if (!payloads.length) {
          container.innerHTML = '<p class="empty">No payloads received yet.</p>';
          return;
        }

        container.innerHTML = payloads.map((entry) => `
          <article class="payload">
            <h3>${entry.timestamp_utc || "Unknown timestamp"}</h3>
            <pre>${entry.pretty_json}</pre>
          </article>
        `).join("");
      } catch (error) {
        container.innerHTML = '<p class="empty">Unable to load payloads from localhost.</p>';
      }
    }

    refreshPayloads();
    setInterval(refreshPayloads, 1500);
  </script>
</body>
</html>
"""


def _localhost_only(client_ip: str) -> bool:
    return client_ip in {HOST, "127.0.0.1", "::1"}


class LocalOnlyHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        if not _localhost_only(self.client_address[0]):
            self.send_error(HTTPStatus.FORBIDDEN, "Only localhost is allowed")
            return

        path = urlparse(self.path).path
        if path == "/":
            self._send_html(HTML_PAGE)
            return
        if path == "/ingest":
            self._send_html(
                "<html><body><h1>Receiver is running</h1>"
                "<p>This endpoint accepts POST requests from the safe demo.</p>"
                '<p>Open <a href="/">the monitor page</a> to view incoming payloads.</p>'
                "</body></html>"
            )
            return
        if path == "/api/payloads":
            self._send_json(list(RECENT_PAYLOADS))
            return

        self.send_error(HTTPStatus.NOT_FOUND, "Page not found")

    def do_POST(self) -> None:  # noqa: N802
        if not _localhost_only(self.client_address[0]):
            self.send_error(HTTPStatus.FORBIDDEN, "Only localhost is allowed")
            return

        path = urlparse(self.path).path
        if path != "/ingest":
            self.send_error(HTTPStatus.NOT_FOUND, "Unknown endpoint")
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(content_length).decode("utf-8")
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self.send_error(HTTPStatus.BAD_REQUEST, "Invalid JSON payload")
            return

        pretty_json = json.dumps(data, indent=2)
        RECENT_PAYLOADS.appendleft(
            {
                "timestamp_utc": data.get("timestamp_utc", "unknown"),
                "pretty_json": escape(pretty_json),
            }
        )

        print("Received payload:")
        print(pretty_json)

        self._send_json({"status": "ok", "message": "Payload received"})

    def _send_html(self, body: str) -> None:
        encoded = body.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def _send_json(self, payload: object) -> None:
        encoded = json.dumps(payload).encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, format: str, *args: object) -> None:
        return


def main() -> None:
    server = HTTPServer((HOST, PORT), LocalOnlyHandler)
    print(f"Local receiver listening on http://{HOST}:{PORT}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
