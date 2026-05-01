import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config

class ValidationService:
    @staticmethod
    def generate_otp(length=6):
        return ''.join(random.choices(string.digits, k=length))

    @staticmethod
    def send_email(subject, body, to_email):
        try:
            msg = MIMEMultipart()
            msg['From'] = Config.SMTP_USER
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT)
            server.starttls()
            server.login(Config.SMTP_USER, Config.SMTP_PASS)
            server.send_message(msg)
            server.quit()
            return True
        except Exception as e:
            print(f"Email Error: {e}")
            return False
