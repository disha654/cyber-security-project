from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, Campaign, Template, Target, Event
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///phishing.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev-secret-key'

db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    campaigns = Campaign.query.all()
    templates = Template.query.all()
    targets = Target.query.all()
    return render_template('admin/index.html', campaigns=campaigns, templates=templates, targets=targets)

# Template Management
@app.route('/templates', methods=['GET', 'POST'])
def manage_templates():
    if request.method == 'POST':
        name = request.form.get('name')
        subject = request.form.get('subject')
        body = request.form.get('body')
        new_template = Template(name=name, subject=subject, body=body)
        db.session.add(new_template)
        db.session.commit()
        return redirect(url_for('manage_templates'))
    templates = Template.query.all()
    return render_template('admin/templates.html', templates=templates)

# Target Management
@app.route('/targets', methods=['GET', 'POST'])
def manage_targets():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        if not Target.query.filter_by(email=email).first():
            new_target = Target(email=email, name=name)
            db.session.add(new_target)
            db.session.commit()
        return redirect(url_for('manage_targets'))
    targets = Target.query.all()
    return render_template('admin/targets.html', targets=targets)

# Campaign Management
@app.route('/campaigns/new', methods=['POST'])
def create_campaign():
    name = request.form.get('name')
    template_id = request.form.get('template_id')
    new_campaign = Campaign(name=name, template_id=template_id)
    db.session.add(new_campaign)
    db.session.commit()
    return redirect(url_for('index'))

# Tracking Route (The Phishing Link)
@app.route('/p/<int:target_id>/<int:campaign_id>')
def phish_link(target_id, campaign_id):
    # Log the click
    event = Event(
        campaign_id=campaign_id,
        target_id=target_id,
        type='click',
        user_agent=request.headers.get('User-Agent'),
        ip_address=request.remote_addr
    )
    db.session.add(event)
    db.session.commit()
    
    campaign = Campaign.query.get(campaign_id)
    return render_template('phish/template.html', campaign=campaign, target_id=target_id)

# Form Submission Tracking
@app.route('/submit/<int:target_id>/<int:campaign_id>', methods=['POST'])
def phish_submit(target_id, campaign_id):
    # Log the submission (DO NOT STORE PASSWORDS)
    event = Event(
        campaign_id=campaign_id,
        target_id=target_id,
        type='submit',
        user_agent=request.headers.get('User-Agent'),
        ip_address=request.remote_addr
    )
    db.session.add(event)
    db.session.commit()
    return redirect(url_for('education'))

@app.route('/education')
def education():
    return render_template('education/index.html')

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# SMTP Configuration (Defaulting to localhost for Sendmail/Postfix)
SMTP_SERVER = "localhost"
SMTP_PORT = 1025 # MailHog default port for testing
SMTP_USER = ""
SMTP_PASSWORD = ""
FROM_EMAIL = "security-training@yourdomain.com"

def send_phishing_email(target, campaign, phish_url):
    try:
        msg = MIMEMultipart()
        msg['From'] = FROM_EMAIL
        msg['To'] = target.email
        msg['Subject'] = campaign.template.subject
        
        # Inject the phish link into the template body
        body = campaign.template.body.replace("{{link}}", phish_url)
        msg.attach(MIMEText(body, 'html'))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            if SMTP_USER and SMTP_PASSWORD:
                server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Error sending to {target.email}: {e}")
        return False

# Campaign Launch
@app.route('/campaigns/<int:campaign_id>/launch', methods=['POST'])
def launch_campaign(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    targets = Target.query.all()
    
    success_count = 0
    for target in targets:
        phish_url = f"http://localhost:5000/p/{target.id}/{campaign.id}"
        if send_phishing_email(target, campaign, phish_url):
            success_count += 1
            
    return jsonify({"status": "launched", "sent": success_count, "total": len(targets)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
