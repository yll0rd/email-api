from tortoise import models, fields

from tortoise.contrib.pydantic import pydantic_model_creator

class EmailReq(models.Model):
    id = fields.IntField(pk=True)
    sender_email = fields.CharField(max_length=255)
    receiver_email = fields.CharField(max_length=255)
    subject = fields.CharField(max_length=255)
    body = fields.TextField()

Email_Model = pydantic_model_creator(EmailReq, name="Email")

