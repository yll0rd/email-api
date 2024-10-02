import os
from ssl import create_default_context

from fastapi import FastAPI, responses
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import Optional
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Email-Sender")

# OWN_EMAIL = "elcappicio@gmail.com"
# OWN_EMAIL_PASSWORD = "123admin#"
BASE_URL = os.getenv("BASE_URL", ' http://127.0.0.1:8000 ')


# OWN_EMAIL = os.getenv("MAIL_ADDRESS", 'youmbileo14@gmail.com')
# OWN_EMAIL_PASSWORD = os.getenv("MAIL_PASSWORD", 'qrpasmjzbhqrqexh')
# OWN_EMAIL = os.getenv("MAIL_ADDRESS", 'njingtishanelle@gmail.com')
# OWN_EMAIL_PASSWORD = os.getenv("MAIL_PASSWORD", 'mail_address')


class EmailBody(BaseModel):
    sender_email: Optional[str] = None
    sender_password: Optional[str] = None
    receiver_email: str
    subject: str
    body: str


@app.get("/")
async def health_check():
    base_url = BASE_URL.lstrip().rstrip()
    target_url = f"{base_url}/redoc"
    return RedirectResponse(url=target_url)
    # return "The health check is successful"


@app.post("/send_email", response_class=responses.JSONResponse)
async def send_email(em: EmailBody):
    mail_address = em.sender_email or "youmbileo14@gmail.com"
    mail_password = em.sender_password or "qrpasmjzbhqrqexh"

    ctx = create_default_context()  # creates a secure SSL context to ensure that the connection to the SMTP server
    # is encrypted.

    try:
        with SMTP("smtp.gmail.com", 587) as email_client:
            email_client.ehlo()
            email_client.starttls(context=ctx)  # Upgrades the connection to a secure encrypted SSL/TLS connection using the previously created context.
            email_client.ehlo()
            email_client.login(mail_address, mail_password)

            to_address = em.receiver_email
            subject = em.subject
            body = em.body

            msg = MIMEMultipart()
            # msg['From'] = OWN_EMAIL if em.sender_email is None else em.sender_email
            msg['To'] = to_address
            msg['Subject'] = subject

            # Attach the email body as UTF-8
            msg.attach(MIMEText(body, 'html', 'utf-8'))

            # message = f"Subject: {subject}\n\n{body}"

            email_client.sendmail(mail_address, to_address, msg.as_string())
            email_client.quit()
        return {"status": 200, "errors": None, "message": "Email sent successfully"}
        # return "Email sent successfully"
    except Exception as e:
        return {"status": 500, "errors": e}
