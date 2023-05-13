from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import register_tortoise, HTTPNotFoundError
from pydantic import BaseModel
from smtplib import SMTP_SSL
from email.mime.text import MIMEText

from models import EmailReq, Email_Model

app = FastAPI(title="Email-Api")

OWN_EMAIL = "elcappicio@gmail.com"
OWN_EMAIL_PASSWORD = "123admin#"

class EmailBody(BaseModel):
    sender_email: str
    receiver_email: str
    subject: str
    body: str

@app.post("/send_email", response_model=Email_Model)
async def send_email(em: EmailBody):
    await EmailReq.create(sender_email=em.sender_email, receiver_email=em.receiver_email, subject=em.subject, body=em.body)
    # return await Email_Model.from_tortoise_orm(obj)
    try:
        msg = MIMEText(body.message, "html")
        msg['Subject'] = em.subject
        msg['From'] = f'Denolyrics <{OWN_EMAIL}>'
        msg['To'] = em.receiver_email

        port = 465  # For SSL

        # Connect to the email server
        server = SMTP_SSL("mail.privateemail.com", port)
        server.login(OWN_EMAIL, OWN_EMAIL_PASSWORD)

        # Send the email
        server.send_message(msg)
        server.quit()
        return {"message": "Email sent successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={'models': ['models']},
    generate_schemas=True,
    add_exception_handlers=True
)