from logging import getLogger

logger = getLogger(__name__)


class EmailMessage(object):
    def __init__(self, email, message, subject, **kwargs):
        self.email = [email, ] if isinstance(email, str) else email
        self.message = message
        self.subject = subject

    def send(self):
        logger.info("send email to %s, subject: %s, message: %s" % (self.email, self.subject, self.message))
        from {{cookiecutter.project}}.rpc.message.email.django import send_mail
        return send_mail(self.subject, self.message, self.email)
