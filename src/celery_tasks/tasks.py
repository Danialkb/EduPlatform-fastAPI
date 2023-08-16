from email.message import EmailMessage

from celery import Celery
import smtplib

from fastapi import Depends

from config import SMTP_USER, SMTP_PASSWORD
from users.dependencies import get_user_service
from users.services import UserService

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

celery = Celery('tasks', broker='redis://localhost:6379')


async def _get_all_emails(user_service: UserService = Depends(get_user_service)):
    users = await user_service.get_users()

    return [(user.name, user.email) for user in users]


async def _email_message_for_users():
    emails = await _get_all_emails()
    emails_to_send = []
    for i in emails:
        email = EmailMessage()
        email['Subject'] = 'MESSAGE'
        email['From'] = SMTP_USER
        email['To'] = i[1]
        email.set_content(
            '<div>'
            f'<h1 style="color: red;">Здравствуйте, {i[0]}. Зацените новый курс</h1>'
            '</div>',
            subtype='html'
        )
        emails_to_send.append(email)

    return emails_to_send


@celery.task
async def send_new_course_started():
    emails = await _email_message_for_users()
    for email in emails:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(email)

