# Cyber Threat Intelligence (CTI) Dashboard

A real-time dashboard to aggregate threat intelligence from VirusTotal and AbuseIPDB.

## Features
- **Real-time Lookup**: Search IP addresses or domains.
- **Multi-Source Analysis**: Fetches data from VirusTotal and AbuseIPDB.
- **Dashboard**: Visualize lookup metrics and types.
- **History**: Keep track of all past lookups with tagging.
- **Export**: Export history to CSV or JSON.
- **Tagging**: Add custom tags to Indicators of Compromise (IOCs).

## Requirements
- Python 3.8+
- MongoDB (Running on `localhost:27017` by default)
- API Keys for:
    - [VirusTotal](https://www.virustotal.com/)
    - [AbuseIPDB](https://www.abuseipdb.com/)

## Installation

1. **Clone the repository** (if applicable).
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Environment**:
   - Rename `.env.example` to `.env`.
   - Add your API keys and MongoDB URI to the `.env` file.

## Running the Application

1. **Start MongoDB** (Ensure your local MongoDB service is running).
2. **Run the Flask app**:
   ```bash
   python app.py
   ```
3. **Access the dashboard**:
   Open `http://127.0.0.1:5000` in your browser.

## Project Structure
- `app.py`: Main Flask application.
- `services/api_client.py`: API integration logic.
- `services/db.py`: MongoDB interaction.
- `templates/`: HTML templates.
- `static/`: CSS/JS and assets.
