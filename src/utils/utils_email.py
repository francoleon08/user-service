import os
from dotenv import load_dotenv
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from jinja2 import FileSystemLoader, Environment

load_dotenv()

template_loader = FileSystemLoader(searchpath="./templates")
template_env = Environment(loader=template_loader)


async def send_verification_email(user_email: str, username: str, verification_code: str):
    template = template_env.get_template('verification_email.html')
    html_content = template.render(username=username, verification_code=verification_code)

    message = MessageSchema(
        subject="Verification Email - Price comparison",
        recipients=[user_email],
        body=html_content,
        subtype='html',
    )

    connection_config = ConnectionConfig(
        MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
        MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
        MAIL_PORT=int(os.getenv('MAIL_PORT')),
        MAIL_SERVER=os.getenv('MAIL_SERVER'),
        MAIL_FROM=os.getenv('MAIL_FROM'),
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False
    )

    fm = FastMail(connection_config)
    await fm.send_message(message)
