from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email(subject, plain_message, html_message, from_email, emails):
    send_mail(
        subject=subject,
        message=plain_message,
        html_message=html_message,
        from_email=from_email,
        recipient_list=emails,
    )
