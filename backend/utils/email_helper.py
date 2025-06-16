import smtplib
from email.message import EmailMessage
from config import Config
from dotenv import load_dotenv
import os

load_dotenv()

def send_email(to_email, subject, body, attachment_path=None):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = Config.MAIL_USERNAME
    msg['To'] = to_email
    msg.set_content(body)

    # ✅ Attach file if path is provided
    if attachment_path:
        try:
            with open(attachment_path, 'rb') as f:
                file_data = f.read()
                file_name = os.path.basename(attachment_path)
                msg.add_attachment(
                    file_data,
                    maintype='application',
                    subtype='octet-stream',
                    filename=file_name
                )
        except Exception as e:
            print(f"❌ Error attaching file: {e}")
            return

    try:
        with smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT) as server:
            server.starttls()
            server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
            server.send_message(msg)
        print(f"✅ Email sent to {to_email}")
    except Exception as e:
        print(f"❌ Error sending email: {e}")
