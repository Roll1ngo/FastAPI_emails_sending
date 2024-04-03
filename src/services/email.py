from pathlib import Path
from dotenv import load_dotenv
import os

from pydantic import EmailStr
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType

from src.services.auth import auth_service

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=os.getenv("MAIL_PORT"),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_FROM_NAME="HW13_Test",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path('templates')
)


async def send_email(email: EmailStr, username=str, host=str):
    try:
        token_verification = auth_service.create_email_token({"sub": email})
        message = MessageSchema(
            subject="Verify your email",
            recipients=[email],
            template_body={"host": host, "username": username, "email": email, "token": token_verification},
            subtype=MessageType.html
        )

        fm = FastMail(conf)

        await fm.send_message(message, template_name="verify_email.html")
    except ConnectionError as err:
        print(err)
