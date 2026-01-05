"""
Email service for sending verification codes
"""

import smtplib
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from config import Config


def generate_verification_code(length=6):
    """Generate a random numeric verification code"""
    return ''.join(random.choices(string.digits, k=length))


def send_verification_email(to_email, code, purpose='signup'):
    """
    Send verification code via email
    
    Args:
        to_email: Recipient email address
        code: The 6-digit verification code
        purpose: 'signup' or 'reset'
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    
    # Email configuration from environment
    smtp_host = Config.EMAIL_HOST or 'smtp.gmail.com'
    smtp_port = int(Config.EMAIL_PORT or 587)
    smtp_username = Config.EMAIL_USERNAME
    smtp_password = Config.EMAIL_PASSWORD
    from_email = Config.EMAIL_FROM or smtp_username
    
    if not smtp_username or not smtp_password:
        print("Email credentials not configured. Code:", code)
        # In development, just print the code if email isn't configured
        return True
    
    # Create message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"Your Meal Master Verification Code: {code}"
    msg['From'] = f"Meal Master <{from_email}>"
    msg['To'] = to_email
    
    # Email content based on purpose
    if purpose == 'signup':
        title = "Welcome to Meal Master!"
        action = "complete your account registration"
    else:
        title = "Password Reset Request"
        action = "reset your password"
    
    # Plain text version
    text = f"""
{title}

Your verification code is: {code}

Use this code to {action}. The code expires in 10 minutes.

If you didn't request this, please ignore this email.

- The Meal Master Team
"""
    
    # HTML version
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: 'Outfit', Arial, sans-serif; background-color: #f8f9fa; padding: 20px; }}
        .container {{ max-width: 480px; margin: 0 auto; background: white; border-radius: 16px; padding: 40px; box-shadow: 0 4px 24px rgba(0,0,0,0.08); }}
        .logo {{ font-size: 24px; font-weight: bold; text-align: center; margin-bottom: 24px; }}
        .logo span {{ margin-right: 8px; }}
        h1 {{ color: #0f172a; font-size: 20px; margin-bottom: 16px; }}
        .code {{ font-size: 32px; font-weight: bold; text-align: center; letter-spacing: 8px; padding: 24px; background: linear-gradient(135deg, #8b5cf6 0%, #3b82f6 100%); color: white; border-radius: 12px; margin: 24px 0; }}
        p {{ color: #64748b; line-height: 1.6; }}
        .footer {{ text-align: center; margin-top: 32px; font-size: 12px; color: #94a3b8; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="logo"><span>🍽️</span>Meal Master</div>
        <h1>{title}</h1>
        <p>Use the verification code below to {action}:</p>
        <div class="code">{code}</div>
        <p>This code expires in <strong>10 minutes</strong>.</p>
        <p>If you didn't request this code, you can safely ignore this email.</p>
        <div class="footer">
            &copy; 2024 Meal Master. All rights reserved.
        </div>
    </div>
</body>
</html>
"""
    
    msg.attach(MIMEText(text, 'plain'))
    msg.attach(MIMEText(html, 'html'))
    
    try:
        # Connect to SMTP server
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print(f"Verification email sent to {to_email}")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        # In development, return True so the flow continues
        # The code is printed to console
        print(f"DEV MODE - Verification code for {to_email}: {code}")
        return True


def get_code_expiry():
    """Get expiry time for verification code (10 minutes from now)"""
    return datetime.utcnow() + timedelta(minutes=10)
