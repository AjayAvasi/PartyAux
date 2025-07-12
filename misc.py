import random
import smtplib
from email.mime.text import MIMEText
import jwt
from datetime import datetime
import db
from dotenv import load_dotenv
import os

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
    body = f"""
    <html>
    <body style='font-family: Arial, sans-serif; background: #f9f9f9; padding: 30px;'>
        <div style='max-width: 400px; margin: auto; background: #fff; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); padding: 30px; text-align: center;'>
            <h2 style='color: #6C63FF; margin-bottom: 10px;'>PartyAux</h2>
            <p style='font-size: 18px; color: #333; margin-bottom: 20px;'>Your One-Time Password (OTP) for <b>Login</b>:</p>
            <div style='font-size: 32px; font-weight: bold; letter-spacing: 6px; color: #222; background: #f3f3f3; border-radius: 8px; padding: 16px 0; margin-bottom: 20px;'>{otp}</div>
            <p style='color: #666; font-size: 15px;'>Please use this code to complete your login to PartyAux.<br/>This code <b>expires in 10 minutes</b>.<br/>If you did not request this, you can safely ignore this email.</p>
            <div style='margin-top: 30px; color: #aaa; font-size: 13px;'>PartyAux &copy; 2025</div>
        </div>
    </body>
    </html>
    """
    send_email(email, subject, body)

def create_jwt(email):
    return jwt.encode({"email": email, "timestamp": datetime.now().timestamp()}, os.getenv('JWT_SECRET', 'your_jwt_secret_here'), algorithm=os.getenv('JWT_ALGORITHM', 'HS256'))

def create_room_code():
    code = ''.join(random.choices('0123456789', k=6))
    while db.room_exists(code):
        code = ''.join(random.choices('0123456789', k=6))
    return code

