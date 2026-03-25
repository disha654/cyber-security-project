from app import app, db
from models import Template, Target

def seed():
    with app.app_context():
        # Add a default template
        if not Template.query.first():
            t1 = Template(
                name="Microsoft Office 365 Login",
                subject="Action Required: Your Office 365 account is locked",
                body="""
                <html>
                <body>
                    <h2>Security Alert</h2>
                    <p>We detected unusual activity on your account. To prevent unauthorized access, we have temporarily locked it.</p>
                    <p>Please log in here to verify your identity: <a href="{{link}}">Verify Account</a></p>
                    <p>Failure to do so within 24 hours will result in permanent suspension.</p>
                    <br>
                    <p>Thanks,<br>Microsoft Security Team</p>
                    <hr>
                    <p style="font-size: 10px; color: gray;">This is an ethical phishing simulation for training purposes.</p>
                </body>
                </html>
                """
            )
            db.session.add(t1)
        
        # Add a test target
        if not Target.query.first():
            target1 = Target(email="testuser@example.com", name="Test User")
            db.session.add(target1)
        
        db.session.commit()
        print("Database seeded with default template and target.")

if __name__ == "__main__":
    seed()
