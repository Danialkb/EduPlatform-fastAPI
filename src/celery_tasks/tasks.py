from celery import Celery
import smtplib

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

celery = Celery('tasks', broker='redis://localhost:6379')


@celery.task
def send_new_course_started():
    ...

