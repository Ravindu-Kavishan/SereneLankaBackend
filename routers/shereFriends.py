from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sF_router = APIRouter()

# Define the request body schema
class EmailRequest(BaseModel):
    to_email: EmailStr
    subject: str|None ="Test Email"
    body: str|None ="This is a test email from FastAPI."

# Email sending endpoint
@sF_router.post("/send-email/")
async def send_email(email_request: EmailRequest):
    sender_email = "r.k.fashionkurunegala@gmail.com"  # Replace with your email
    sender_password = "ifou lnky aiot hoim"     # Replace with your email password (use app password for Gmail)
    smtp_server = "smtp.gmail.com"        # Replace with your SMTP server
    smtp_port = 587                       # Replace with your SMTP port

    # Create the email message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = email_request.to_email
    message["Subject"] = email_request.subject

    # Attach the email body
    message.attach(MIMEText(email_request.body, "plain"))

    try:
        # Connect to the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email_request.to_email, message.as_string())
        return {"message": "Email sent successfully!"}
    except smtplib.SMTPException as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {e}")
