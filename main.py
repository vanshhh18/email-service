from fastapi import FastAPI
from pydantic import BaseModel
import smtplib
from email.mime.text import MIMEText
import os

app = FastAPI()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


class EmailRequest(BaseModel):
    to: str
    ticket_id: str
    department: str
    priority: str
    user_ticket: str
    ai_response: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/send-email")
def send_email(req: EmailRequest):
    subject = f"Support Ticket Created - #{req.ticket_id}"
    body = f"""
Hello,

Thank you for contacting us. Your support ticket has been received.

Ticket ID:   #{req.ticket_id}
Department:  {req.department}
Priority:    {req.priority}

Your Issue:
{req.user_ticket}

AI Analysis:
{req.ai_response}

Our support team will investigate and get back to you shortly.

Regards,
AI Helpdesk Team
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = req.to

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        return {"status": "sent"}
    except Exception as e:
        return {"status": "failed", "error": str(e)}
