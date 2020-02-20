from django.utils.html import strip_tags
from django.core.mail import send_mail as _send_mail
from django.conf import settings


def send_mail(subject, body, to_emails, from_email=settings.EMAIL_FROM):
    text_content = strip_tags(body)
    if _send_mail(
        subject,
        text_content,
        from_email,
        to_emails,
        html_message=body,
        fail_silently=False,
    ):
        return True
    return False
