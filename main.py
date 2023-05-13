from fastapi import FastAPI, HTTPException, responses
from tortoise.contrib.fastapi import register_tortoise, HTTPNotFoundError
from pydantic import BaseModel
from smtplib import SMTP

from models import EmailReq, Email_Model

app = FastAPI(title="Email-Api")

OWN_EMAIL = "elcappicio@gmail.com"
OWN_EMAIL_PASSWORD = "123admin#"

class EmailBody(BaseModel):
    sender_email: str
    receiver_email: str
    subject: str
    body: str

@app.post("/send_email", response_class=responses.PlainTextResponse)
async def send_email(em: EmailBody):
    await EmailReq.create(sender_email=em.sender_email, receiver_email=em.receiver_email, subject=em.subject, body=em.body)
    # return await Email_Model.from_tortoise_orm(obj)
    email_client = SMTP("smtp.gmail.com", 587)
    email_client.starttls()
    email_client.login(OWN_EMAIL, OWN_EMAIL_PASSWORD)

    to_address = em.receiver_email
    subject = em.subject
    body = em.body
    
    message = f"Subject: {subject}\n\n{body}"

    email_client.sendmail(OWN_EMAIL, to_address, message)
    email_client.quit()

    return "Email sent successfully"

register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={'models': ['models']},
    generate_schemas=True,
    add_exception_handlers=True
)