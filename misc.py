import random
import smtplib
from email.mime.text import MIMEText
import jwt
from datetime import datetime
import db
from dotenv import load_dotenv
import os
from email_templates import get_otp_email_html

# Load environment variables
load_dotenv()

sender_email = os.getenv('SENDER_EMAIL', "your_email@gmail.com")
sender_password = os.getenv('SENDER_PASSWORD', "your_app_password_here")

smtp_server = os.getenv('SMTP_SERVER', "smtp.gmail.com")
smtp_port = int(os.getenv('SMTP_PORT', "587"))                       

def generate_otp(length = 6):
    return ''.join(random.choices('0123456789', k=length))

def send_email(email, subject, body):
    message = MIMEText(body, 'html')
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls() 
            server.login(sender_email, sender_password)
            server.send_message(message)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

def send_otp(email, otp):
    subject = "Your PartyAux Login OTP Code"
    body = get_otp_email_html(otp)
    send_email(email, subject, body)

def create_jwt(email):
    return jwt.encode({"email": email, "timestamp": datetime.now().timestamp()}, os.getenv('JWT_SECRET', 'your_jwt_secret_here'), algorithm=os.getenv('JWT_ALGORITHM', 'HS256'))

def create_room_code():
    code = ''.join(random.choices('0123456789', k=6))
    while db.room_exists(code):
        code = ''.join(random.choices('0123456789', k=6))
    return code

def create_jwt(email):
    return jwt.encode({"email": email, "timestamp": datetime.now().timestamp()}, os.getenv('JWT_SECRET', 'your_jwt_secret_here'), algorithm=os.getenv('JWT_ALGORITHM', 'HS256'))

def create_room_code():
    code = ''.join(random.choices('0123456789', k=6))
    while db.room_exists(code):
        code = ''.join(random.choices('0123456789', k=6))
    return code

