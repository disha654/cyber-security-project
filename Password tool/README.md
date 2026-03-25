# Password Security Toolkit

Password Security Toolkit is a full-stack web app for:

- Password strength analysis
- Custom wordlist generation for authorized security testing
- Downloading generated wordlists in `.txt` format

## Stack

- Frontend: Next.js + React + Bootstrap
- Backend: Flask (Python)
- Deployment target: Vercel (Next.js + Python serverless runtime)

## Features

- Color-coded password strength indicator
- Strength progress bar
- Password visibility toggle
- Loading states for API operations
- Wordlist preview + `.txt` download
- Pattern generation with capitalization, leetspeak, common suffixes, and year appends

## Project Structure

- `app/` - Next.js frontend UI
- `api/index.py` - Flask API routes for analyze/generate/download
- `password_tool/` - Shared Python logic for analysis and wordlist generation
- `vercel.json` - Vercel routing/runtime config

## Local Setup

1. Create/activate virtual environment (already available in this project):

```powershell
.\venv\Scripts\Activate.ps1
```

2. Install Python dependencies:

```powershell
.\venv\Scripts\pip.exe install -r requirements.txt
```

3. Install Node dependencies:

```powershell
npm install
```

4. Run local development (frontend + backend):

```powershell
npm run dev
```

5. Open:

- `http://localhost:3000`

## API Endpoints

- `GET /api/health`
- `POST /api/analyze`
- `POST /api/generate`
- `POST /api/download`

### Sample Analyze Payload

```json
{
  "password": "password123"
}
```

### Sample Generate Payload

```json
{
  "name": "john",
  "nickname": "rocky",
  "dob": "2001",
  "keyword": "hacker"
}
```

## Vercel Deployment

1. Push project to GitHub.
2. Import repository into Vercel.
3. Deploy.

Vercel will use:

- Next.js app for frontend routes
- `api/index.py` for serverless Python API routes

## Important

Use this tool only for educational purposes and authorized security testing.
