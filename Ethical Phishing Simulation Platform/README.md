# Ethical Phishing Simulation Platform

A professional-grade phishing simulation tool designed for organizations to conduct security awareness training. This platform allows administrators to create campaigns, manage targets, and track the effectiveness of phishing simulations in a controlled environment.

## Features

- **Campaign Management**: Create and launch targeted phishing campaigns.
- **Template Builder**: Design realistic phishing emails with dynamic placeholders.
- **Target Tracking**: Manage lists of employees or targets for training.
- **Real-time Analytics**: Track email opens, link clicks, and form submissions.
- **Educational Landing Pages**: Automatically redirect "phished" users to educational content.
- **SQLite Database**: Lightweight and portable data storage for campaigns and events.

## Tech Stack

- **Backend**: Python (Flask)
- **Database**: SQLAlchemy (SQLite)
- **Frontend**: HTML/CSS (Jinja2 Templates)
- **Email**: Python `smtplib`

## Getting Started

1. Install dependencies:
   ```bash
   pip install flask flask-sqlalchemy
   ```
2. Run the application:
   ```bash
   python app.py
   ```
3. Access the admin dashboard at `http://localhost:5000`.

## Disclaimer

This tool is for **educational and ethical security testing purposes only**. Unauthorized use of this platform against targets without explicit consent is illegal and unethical.
