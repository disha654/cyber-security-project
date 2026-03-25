# Log File Analyzer for Intrusion Detection

A Python-based tool to analyze Apache and SSH logs for suspicious activity, including brute-force attacks, DoS attempts, and vulnerability scanning. It generates alerts in CSV format and visualizations of access patterns.

## Features

- **Log Parsing**: Supports Apache Access Logs and SSH Authentication Logs.
- **Threat Detection**:
  - **Brute Force**: Detects high frequency of failed SSH logins from a single IP.
  - **DoS Detection**: Flags IPs with unusually high request rates in a short window.
  - **Vulnerability Scanning**: Identifies IPs generating 404/403 errors or scanning for sensitive paths.
  - **Blacklist Check**: Cross-references IPs against a simulated threat intelligence list.
- **Reporting**: Exports detailed CSV alerts and generates PNG charts for top source IPs and HTTP methods.

## Prerequisites

- Python 3.x
- `pandas`
- `matplotlib`
- `requests`

## Installation

1.  Clone or download this repository.
2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Prepare Logs**: Ensure your log files are in the `logs/` directory.
    - Default Apache log path: `logs/apache_access.log`
    - Default SSH log path: `logs/ssh_auth.log`
    *(Sample logs are automatically created if you run the setup script or use the provided samples)*

2.  **Run the Analyzer**:
    ```bash
    python app.py
    ```

3.  **View Reports**:
    - Check the console output for a summary of detected threats.
    - Navigate to the `reports/` directory to view detailed CSV alerts and visualization charts.

## Output Files (in `reports/`)

- `brute_force_alerts.csv`: IPs exceeding failed login thresholds.
- `dos_alerts.csv`: IPs exceeding request rate limits.
- `scanning_alerts.csv`: IPs with high error rates or suspicious path access.
- `blacklisted_apache.csv` / `blacklisted_ssh.csv`: IPs found in the blocklist.
- `top_ips_apache.png`: Chart of most active IPs in Apache logs.
- `top_methods_apache.png`: Chart of HTTP method distribution.
