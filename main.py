import os

from fastapi import FastAPI, responses
from pydantic import BaseModel
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Email-Sender")

# OWN_EMAIL = "elcappicio@gmail.com"
# OWN_EMAIL_PASSWORD = "123admin#"
OWN_EMAIL = os.getenv("MAIL_ADDRESS", 'youmbileo14@gmail.com')
OWN_EMAIL_PASSWORD = os.getenv("MAIL_PASSWORD", 'qrpasmjzbhqrqexh')


class EmailBody(BaseModel):
    # sender_email: str
    receiver_email: str
    subject: str
    body: str


@app.get("/")
async def health_check():
    return "The health check is successful"


@app.post("/send_email", response_class=responses.PlainTextResponse)
async def send_email(em: EmailBody):
    email_client = SMTP("smtp.gmail.com", 587)
    email_client.starttls()
    email_client.login(OWN_EMAIL, OWN_EMAIL_PASSWORD)

    to_address = em.receiver_email
    subject = em.subject
    body = em.body

    msg = MIMEMultipart()
    msg['From'] = OWN_EMAIL
    msg['To'] = to_address
    msg['Subject'] = subject

    # Attach the email body as UTF-8
    msg.attach(MIMEText(body, 'html', 'utf-8'))

    # message = f"Subject: {subject}\n\n{body}"

    email_client.sendmail(OWN_EMAIL, to_address, msg.as_string())
    email_client.quit()

    return "Email sent successfully"
